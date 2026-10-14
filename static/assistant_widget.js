/**
 * FitAI Co-Pilot - Global Floating Assistant Widget
 * CreditFit360 - Financial Intelligence System
 */

(function () {
    // Prevent duplicate injection or injection on dedicated /assistant page
    if (window.FitAIAssistantLoaded || window.location.pathname === "/assistant" || window.location.pathname === "/ai-copilot") {
        return;
    }
    window.FitAIAssistantLoaded = true;

    // Load CSS stylesheet if not already present
    if (!document.getElementById("fitai-widget-css")) {
        const link = document.createElement("link");
        link.id = "fitai-widget-css";
        link.rel = "stylesheet";
        link.href = "/static/assistant_widget.css";
        document.head.appendChild(link);
    }

    // Helper to extract financial context from the active page or session
    function getContextFromPage() {
        let ctx = {};
        try {
            const raw = sessionStorage.getItem("creditFitResult");
            if (raw) ctx = JSON.parse(raw);
        } catch (e) { }

        // Also check if user is on form page with active input fields
        const incomeInput = document.getElementById("monthlyIncome") || document.getElementById("monthly_income");
        if (incomeInput && Number(incomeInput.value) > 0) ctx.monthly_income = Number(incomeInput.value);

        const emiInput = document.getElementById("existingEmi") || document.getElementById("existing_emi");
        if (emiInput && Number(emiInput.value) > 0) ctx.existing_emi = Number(emiInput.value);

        const scoreInput = document.getElementById("creditScore") || document.getElementById("credit_score");
        if (scoreInput && Number(scoreInput.value) > 0) ctx.credit_score = Number(scoreInput.value);

        const limitInput = document.getElementById("creditLimit") || document.getElementById("credit_limit");
        if (limitInput && Number(limitInput.value) > 0) ctx.credit_limit = Number(limitInput.value);

        const outInput = document.getElementById("creditOutstanding") || document.getElementById("credit_outstanding");
        if (outInput && Number(outInput.value) > 0) ctx.credit_outstanding = Number(outInput.value);

        return ctx;
    }

    // Markdown simple parser
    function formatWidgetMarkdown(text) {
        if (!text) return "";
        let html = text
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/gim, '<em>$1</em>')
            .replace(/`([^`]+)`/gim, '<code>$1</code>')
            .replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>')
            .replace(/\|(.+)\|/gim, function (match) {
                const cells = match.split('|').filter(c => c.trim() !== '');
                if (cells.some(c => c.includes('---'))) return '';
                return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
            })
            .replace(/\n\n/gim, '<p></p>')
            .replace(/\n/gim, '<br>');

        if (html.includes('<tr>')) {
            html = html.replace(/(<tr>.*?<\/tr>)+/gims, '<table>$1</table>');
        }
        return html;
    }

    // Create Widget DOM
    function initWidget() {
        // 1. Launcher button
        const launcher = document.createElement("div");
        launcher.className = "fitai-launcher";
        launcher.id = "fitaiLauncher";
        launcher.innerHTML = `
            <div class="fitai-launcher-icon">
                🤖
                <div class="fitai-launcher-pulse"></div>
            </div>
            <span class="fitai-launcher-label">FitAI Co-Pilot</span>
            <span class="fitai-launcher-badge">AI</span>
        `;

        // 2. Chat Window
        const windowEl = document.createElement("div");
        windowEl.className = "fitai-window";
        windowEl.id = "fitaiWindow";
        windowEl.innerHTML = `
            <div class="fitai-header">
                <div class="fitai-header-left">
                    <div class="fitai-header-avatar">🤖</div>
                    <div>
                        <div class="fitai-header-title">FitAI Co-Pilot</div>
                        <div class="fitai-header-status">● Financial Advisory Active</div>
                    </div>
                </div>
                <div class="fitai-header-actions">
                    <a href="/assistant" class="fitai-header-btn" title="Expand Full Page" target="_blank">⤢</a>
                    <button class="fitai-header-btn" id="fitaiCloseBtn" title="Close">✕</button>
                </div>
            </div>

            <div class="fitai-body" id="fitaiBody">
                <div class="fitai-msg-row fitai-assistant">
                    <div class="fitai-msg-bubble">
                        <h3>👋 Hi! I am FitAI</h3>
                        <p>Your 24/7 credit and borrowing intelligence co-pilot. Ask me how to boost your score, calculate safe loan capacity, or draft a dispute notice!</p>
                    </div>
                </div>
            </div>

            <div class="fitai-typing" id="fitaiTyping">
                <div class="fitai-dot"></div>
                <div class="fitai-dot"></div>
                <div class="fitai-dot"></div>
            </div>

            <div class="fitai-chips" id="fitaiChips">
                <button class="fitai-chip" data-query="How can I raise my credit score by 50 points in 90 days?">🚀 90-Day Booster</button>
                <button class="fitai-chip" data-query="Can I afford a new loan? Calculate my safe borrowing capacity.">🏦 Safe Loan Limit</button>
                <button class="fitai-chip" data-query="How do I reduce my credit card utilization below 30%?">💳 Card Utilization</button>
                <button class="fitai-chip" data-query="Draft an official dispute letter for an erroneous CIBIL entry.">📝 Dispute Notice</button>
            </div>

            <div class="fitai-footer">
                <form id="fitaiForm" class="fitai-input-wrap">
                    <input type="text" id="fitaiInput" placeholder="Ask FitAI anything..." autocomplete="off" required>
                    <button type="submit" class="fitai-send" title="Send message">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </form>
            </div>
        `;

        document.body.appendChild(launcher);
        document.body.appendChild(windowEl);

        // Interaction logic
        const closeBtn = document.getElementById("fitaiCloseBtn");
        const bodyEl = document.getElementById("fitaiBody");
        const formEl = document.getElementById("fitaiForm");
        const inputEl = document.getElementById("fitaiInput");
        const typingEl = document.getElementById("fitaiTyping");
        const chipsEl = document.getElementById("fitaiChips");

        let isOpen = false;
        let history = [];

        function toggleWindow() {
            isOpen = !isOpen;
            if (isOpen) {
                windowEl.classList.add("fitai-open");
                inputEl.focus();
            } else {
                windowEl.classList.remove("fitai-open");
            }
        }

        launcher.addEventListener("click", toggleWindow);
        closeBtn.addEventListener("click", () => {
            isOpen = false;
            windowEl.classList.remove("fitai-open");
        });

        function appendMsg(role, content) {
            const row = document.createElement("div");
            row.className = `fitai-msg-row ${role === 'user' ? 'fitai-user' : 'fitai-assistant'}`;
            const bubble = document.createElement("div");
            bubble.className = "fitai-msg-bubble";
            bubble.innerHTML = formatWidgetMarkdown(content);
            row.appendChild(bubble);
            bodyEl.appendChild(row);
            bodyEl.scrollTop = bodyEl.scrollHeight;
        }

        async function submitQuery(queryText) {
            const q = (queryText || "").trim();
            if (!q) return;

            appendMsg("user", q);
            history.push({ role: "user", content: q });
            inputEl.value = "";
            typingEl.style.display = "flex";
            bodyEl.scrollTop = bodyEl.scrollHeight;

            const context = getContextFromPage();

            try {
                const res = await fetch("/api/assistant-chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        message: q,
                        context: context,
                        history: history
                    })
                });

                const data = await res.json();
                typingEl.style.display = "none";

                if (data && data.reply) {
                    appendMsg("assistant", data.reply);
                    history.push({ role: "assistant", content: data.reply });
                } else {
                    appendMsg("assistant", "Sorry, I could not compute that. Please verify your connection.");
                }
            } catch (err) {
                typingEl.style.display = "none";
                appendMsg("assistant", "⚠️ Server temporarily unreachable.");
            }
        }

        formEl.addEventListener("submit", (e) => {
            e.preventDefault();
            submitQuery(inputEl.value);
        });

        chipsEl.addEventListener("click", (e) => {
            const target = e.target.closest(".fitai-chip");
            if (target && target.dataset.query) {
                submitQuery(target.dataset.query);
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWidget);
    } else {
        initWidget();
    }
})();
