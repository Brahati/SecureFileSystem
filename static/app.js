(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        initSidebar();
        initSendUpload();
        initTextPreview();
    });

    function initSidebar() {
        var toggle = document.getElementById("sidebarToggle");
        var sidebar = document.getElementById("sidebar");
        if (!toggle || !sidebar) return;

        toggle.addEventListener("click", function () {
            sidebar.classList.toggle("open");
            document.body.classList.toggle("sidebar-open");
        });

        document.addEventListener("click", function (e) {
            if (!sidebar.classList.contains("open")) return;
            if (sidebar.contains(e.target) || toggle.contains(e.target)) return;
            sidebar.classList.remove("open");
            document.body.classList.remove("sidebar-open");
        });
    }

    function initSendUpload() {
        var zone = document.getElementById("dropZone");
        var input = document.getElementById("fileInput");
        if (!zone || !input) return;

        var nameEl = document.getElementById("fileName");
        var statusEl = document.getElementById("fileStatus");
        var iconEl = document.getElementById("fileIcon");

        function setFile(file) {
            if (!file) return;
            var dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;

            if (nameEl) nameEl.textContent = file.name;
            if (statusEl) {
                statusEl.textContent = formatSize(file.size) + " — Ready to encrypt";
                statusEl.classList.add("ready");
            }
            if (iconEl) iconEl.classList.add("has-file");
            zone.classList.add("has-file");
        }

        zone.addEventListener("click", function (e) {
            if (e.target === input) return;
            input.click();
        });

        zone.addEventListener("dragover", function (e) {
            e.preventDefault();
            zone.classList.add("dragover");
        });

        zone.addEventListener("dragleave", function () {
            zone.classList.remove("dragover");
        });

        zone.addEventListener("drop", function (e) {
            e.preventDefault();
            zone.classList.remove("dragover");
            if (e.dataTransfer.files.length) setFile(e.dataTransfer.files[0]);
        });

        input.addEventListener("change", function () {
            if (input.files.length) setFile(input.files[0]);
        });
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / 1048576).toFixed(1) + " MB";
    }

    function initTextPreview() {
        var el = document.getElementById("textPreview");
        if (!el) return;
        var src = el.getAttribute("data-src");
        if (!src) return;

        fetch(src)
            .then(function (r) { return r.text(); })
            .then(function (text) {
                var pre = document.createElement("pre");
                var code = document.createElement("code");
                code.textContent = text;
                pre.appendChild(code);
                el.appendChild(pre);
            })
            .catch(function () {
                el.innerHTML = "<p class=\"preview-error\">Unable to load text preview.</p>";
            });
    }
})();
