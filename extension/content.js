console.log("PhoenixRPA content.js loaded");

// ============================================================
// SELECTOR GENERATOR
// ============================================================

function getSelector(element) {

    if (!element) {
        return "";
    }

    // 1. ID
    if (element.id && element.id.trim() !== "") {
        return `#${CSS.escape(element.id)}`;
    }

    // 2. Name
    if (element.name && element.name.trim() !== "") {
        return `[name="${CSS.escape(element.name)}"]`;
    }

    // 3. data-testid
    const testId = element.getAttribute("data-testid");

    if (testId && testId.trim() !== "") {
        return `[data-testid="${CSS.escape(testId)}"]`;
    }

    // 4. aria-label
    const aria = element.getAttribute("aria-label");

    if (aria && aria.trim() !== "") {
        return `[aria-label="${CSS.escape(aria)}"]`;
    }

    // 5. Placeholder
    const placeholder = element.getAttribute("placeholder");

    if (placeholder && placeholder.trim() !== "") {
        return `[placeholder="${CSS.escape(placeholder)}"]`;
    }

    // 6. Type
    const type = element.getAttribute("type");

    if (type && type.trim() !== "") {
        return `${element.tagName.toLowerCase()}[type="${CSS.escape(type)}"]`;
    }

    // 7. Stable class
    if (
        element.classList &&
        element.classList.length > 0
    ) {

        const className = [...element.classList].find(
            cls =>
                cls &&
                !cls.startsWith("css-") &&
                !cls.startsWith("sc-")
        );

        if (className) {
            return `.${CSS.escape(className)}`;
        }
    }

    // 8. Link text
    if (
        element.tagName &&
        element.tagName.toLowerCase() === "a" &&
        element.textContent &&
        element.textContent.trim() !== ""
    ) {
        return `a:text("${element.textContent.trim()}")`;
    }

    // 9. Button text
    if (
        element.tagName &&
        element.tagName.toLowerCase() === "button" &&
        element.textContent &&
        element.textContent.trim() !== ""
    ) {
        return `button:text("${element.textContent.trim()}")`;
    }

    // 10. Tag fallback
    if (element.tagName) {
        return element.tagName.toLowerCase();
    }

    return "";
}


// ============================================================
// SEND EVENT TO BACKGROUND
// ============================================================

function sendEvent(data) {

    console.log(
        "PhoenixRPA → Background:",
        data
    );

    try {

        chrome.runtime.sendMessage(
            {
                type: "RECORDER_EVENT",
                event: data
            },
            (response) => {

                if (chrome.runtime.lastError) {

                    console.error(
                        "PhoenixRPA extension error:",
                        chrome.runtime.lastError.message
                    );

                    return;
                }

                console.log(
                    "PhoenixRPA background response:",
                    response
                );
            }
        );

    } catch (error) {

        console.error(
            "PhoenixRPA sendEvent error:",
            error
        );
    }
}


// ============================================================
// CLICK RECORDING
// ============================================================

document.addEventListener(
    "click",
    (event) => {

        const target = event.target;
        if (
            location.hostname === "127.0.0.1" ||
            location.hostname === "localhost"
        ) {
            return;
        }

        if (!(target instanceof Element)) {
            return;
        }

        const selector = getSelector(target);

        if (!selector) {
            return;
        }

        console.log(
            "PhoenixRPA Click:",
            selector
        );

        sendEvent({
            action: "click",
            selector: selector
        });

    },
    true
);


// ============================================================
// FILL RECORDING
//
// IMPORTANT:
// We DO NOT record every "input" event.
//
// Instead:
//   input  -> remember latest value
//   blur   -> record final value once
//
// This prevents:
// t
// te
// tes
// test
// test1
// test12
// test123
//
// and records only:
// test123
// ============================================================

const pendingValues = new WeakMap();

document.addEventListener(
    "input",
    (event) => {

        const target = event.target;

        if (!(target instanceof HTMLElement)) {
            return;
        }

        if (
            target.tagName !== "INPUT" &&
            target.tagName !== "TEXTAREA" &&
            !target.isContentEditable
        ) {
            return;
        }

        let value = "";

        if (target.isContentEditable) {
            value = target.innerText || "";
        } else {
            value = target.value || "";
        }

        pendingValues.set(
            target,
            value
        );

    },
    true
);


// ============================================================
// RECORD FINAL VALUE WHEN FIELD LOSES FOCUS
// ============================================================

document.addEventListener(
    "blur",
    (event) => {

        const target = event.target;

        if (!(target instanceof HTMLElement)) {
            return;
        }

        if (
            target.tagName !== "INPUT" &&
            target.tagName !== "TEXTAREA" &&
            !target.isContentEditable
        ) {
            return;
        }

        const selector = getSelector(target);

        if (!selector) {
            return;
        }

        let value;

        if (pendingValues.has(target)) {

            value = pendingValues.get(target);

        } else if (target.isContentEditable) {

            value = target.innerText || "";

        } else {

            value = target.value || "";
        }

        if (!value) {
            return;
        }

        console.log(
            "PhoenixRPA Fill:",
            selector,
            value
        );

        sendEvent({
            action: "fill",
            selector: selector,
            value: value
        });

        pendingValues.delete(target);

    },
    true
);


console.log(
    "PhoenixRPA recorder listeners attached"
);