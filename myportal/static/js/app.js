document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const leftPanel = document.getElementById("leftPanel");
    const leftPanelClose = document.getElementById("leftPanelClose");
    const leftPanelOverlay = document.getElementById("leftPanelOverlay");

    if (!menuToggle || !leftPanel || !leftPanelOverlay) {
        return;
    }

    function openPanel() {
        leftPanel.classList.add("open");
        leftPanel.setAttribute("aria-hidden", "false");
        leftPanelOverlay.hidden = false;
        document.body.classList.add("panel-open");
    }

    function closePanel() {
        leftPanel.classList.remove("open");
        leftPanel.setAttribute("aria-hidden", "true");
        leftPanelOverlay.hidden = true;
        document.body.classList.remove("panel-open");
    }

    menuToggle.addEventListener("click", function () {
        if (leftPanel.classList.contains("open")) {
            closePanel();
        } else {
            openPanel();
        }
    });

    if (leftPanelClose) {
        leftPanelClose.addEventListener("click", closePanel);
    }

    leftPanelOverlay.addEventListener("click", closePanel);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && leftPanel.classList.contains("open")) {
            closePanel();
        }
    });

    document.addEventListener("click", function (event) {
        const clickedLink = event.target.closest("a");
        if (!clickedLink) {
            return;
        }

        const clickInsidePanel = !!event.target.closest("#leftPanel");
        if (!clickInsidePanel && leftPanel.classList.contains("open")) {
            closePanel();
        }
    });
});