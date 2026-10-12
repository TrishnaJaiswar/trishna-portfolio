const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
const navItems = document.querySelectorAll(".nav-link");

menuToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
});

navItems.forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
  });
});

// Reveal sections as they enter the viewport.
const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

// Highlight the current navigation section.
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      navItems.forEach((link) => {
        link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
      });
    }
  });
}, { rootMargin: "-30% 0px -60% 0px" });

document.querySelectorAll("main section[id]").forEach((section) => sectionObserver.observe(section));
document.getElementById("year").textContent = new Date().getFullYear();


// Embedded recruiter-facing RAG chatbot. Configure TRISHNA_CHAT_API_URL to your deployed
// FastAPI base URL (without /api/chat), or leave empty when frontend and API share a host.
const portfolioChatForm = document.getElementById("portfolioChatForm");
if (portfolioChatForm) {
  const chatInput = document.getElementById("portfolioChatInput");
  const chatSend = document.getElementById("portfolioChatSend");
  const chatMessages = document.getElementById("portfolioChatMessages");
  const chatStatus = document.getElementById("portfolioChatStatus");
  const chatHistory = [];
  const apiBase = (window.TRISHNA_CHAT_API_URL || "").replace(/\/$/, "");

  function escapeHtml(value) {
    return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  // Small, safe Markdown renderer for readable ChatGPT-style answers.
  function renderAnswerMarkdown(markdown) {
    const escaped = escapeHtml(markdown || "");
    const inline = (line) => line
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>")
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    const blocks = escaped.trim().split(/\n\s*\n/);
    return blocks.map((block) => {
      const lines = block.split("\n");
      if (lines.every(line => /^\s*[-*]\s+/.test(line))) return '<ul>' + lines.map(line => '<li>' + inline(line.replace(/^\s*[-*]\s+/, "")) + '</li>').join("") + '</ul>';
      if (lines.every(line => /^\s*\d+[.)]\s+/.test(line))) return '<ol>' + lines.map(line => '<li>' + inline(line.replace(/^\s*\d+[.)]\s+/, "")) + '</li>').join("") + '</ol>';
      if (/^#{1,3}\s/.test(lines[0])) {
        const match = lines[0].match(/^(#{1,3})\s+(.*)$/);
        return `<h${match[1].length}>${inline(match[2])}</h${match[1].length}>` + (lines.length > 1 ? '<p>' + lines.slice(1).map(inline).join('<br>') + '</p>' : '');
      }
      return '<p>' + lines.map(inline).join('<br>') + '</p>';
    }).join("");
  }

  function addPortfolioChatMessage(role, text = "", sources = []) {
    const item = document.createElement("article");
    item.className = `portfolio-chat-message ${role}`;
    const label = document.createElement("span");
    label.className = "chat-message-role";
    label.textContent = role === "user" ? "YOU" : "ASK TRISHNA AI";
    const body = document.createElement("div");
    body.className = "chat-message-body";
    if (role === "user") body.textContent = text;
    else body.innerHTML = renderAnswerMarkdown(text);
    item.append(label, body);
    if (sources.length) {
      const sourceLine = document.createElement("div");
      sourceLine.className = "portfolio-chat-sources";
      sourceLine.textContent = `PROFILE SOURCES · ${sources.join(" · ")}`;
      item.append(sourceLine);
    }
    chatMessages.append(item);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return { item, body };
  }

  async function askPortfolioChat(question) {
    addPortfolioChatMessage("user", question);
    const assistant = addPortfolioChatMessage("assistant", "");
    assistant.body.innerHTML = '<span class="chat-typing"><i></i><i></i><i></i></span>';
    chatSend.disabled = true;
    chatInput.disabled = true;
    chatStatus.textContent = "Searching your profile and generating an answer…";
    let fullAnswer = "";
    try {
      const response = await fetch(`${apiBase}/api/chat/stream`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history: chatHistory.slice(-6) })
      });
      if (!response.ok || !response.body) throw new Error(`Chat API returned ${response.status}`);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let sources = [];
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split("\n\n");
        buffer = events.pop() || "";
        for (const event of events) {
          const line = event.split("\n").find(row => row.startsWith("data: "));
          if (!line) continue;
          let payload; try { payload = JSON.parse(line.slice(6)); } catch { continue; }
          if (payload.token) {
            fullAnswer += payload.token;
            assistant.body.innerHTML = renderAnswerMarkdown(fullAnswer);
            chatMessages.scrollTop = chatMessages.scrollHeight;
          }
          if (payload.sources) sources = payload.sources;
          if (payload.error) throw new Error(payload.error);
        }
      }
      if (!fullAnswer.trim()) throw new Error("The assistant returned an empty answer.");
      if (sources.length) {
        const sourceLine = document.createElement("div"); sourceLine.className = "portfolio-chat-sources";
        sourceLine.textContent = `PROFILE SOURCES · ${sources.join(" · ")}`; assistant.item.append(sourceLine);
      }
      chatHistory.push({ role: "user", content: question }, { role: "assistant", content: fullAnswer });
      chatStatus.textContent = "Answers are grounded in retrieved profile information.";
    } catch (error) {
      assistant.body.innerHTML = renderAnswerMarkdown(fullAnswer || "I couldn't connect to the recruiter assistant. Please try again shortly.");
      chatStatus.textContent = "Chat service unavailable. Check that the FastAPI backend is running and configured.";
    } finally {
      chatSend.disabled = false; chatInput.disabled = false; chatInput.focus();
    }
  }

  portfolioChatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const question = chatInput.value.trim();
    if (!question) return;
    chatInput.value = "";
    askPortfolioChat(question);
  });
  document.querySelectorAll("[data-portfolio-question]").forEach((button) => {
    button.addEventListener("click", () => askPortfolioChat(button.dataset.portfolioQuestion));
  });
}
