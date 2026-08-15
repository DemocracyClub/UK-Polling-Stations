(function () {
    "use strict";

    function setStatus(button, message) {
        var container = button.closest("nav");
        var status = container && container.querySelector("[data-site-share-status]");
        if (status) {
            status.textContent = message;
        }
    }

    function copyShareUrl(button) {
        return navigator.clipboard.writeText(button.dataset.shareUrl).then(function () {
            setStatus(button, button.dataset.copySuccess);
        });
    }

    function shareSite(button) {
        var shareData = {
            title: button.dataset.shareTitle,
            text: button.dataset.shareText,
            url: button.dataset.shareUrl
        };

        if (navigator.share) {
            return navigator.share(shareData).catch(function (error) {
                if (error.name === "AbortError") {
                    return;
                }
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    return copyShareUrl(button);
                }
                setStatus(button, button.dataset.shareUnavailable);
            });
        }

        return copyShareUrl(button).catch(function () {
            setStatus(button, button.dataset.copyUnavailable);
        });
    }

    document.querySelectorAll("[data-site-share]").forEach(function (button) {
        if (navigator.share || (navigator.clipboard && navigator.clipboard.writeText)) {
            button.hidden = false;
            button.addEventListener("click", function () {
                shareSite(button);
            });
        }
    });
}());
