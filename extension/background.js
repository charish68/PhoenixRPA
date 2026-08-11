console.log("PhoenixRPA background.js loaded");

// ============================================================
// PHOENIXRPA BACKEND
// ============================================================

const BACKEND_URL = "http://127.0.0.1:8000";

// ============================================================
// RECEIVE EVENTS FROM content.js
// ============================================================

chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        console.log(
            "PhoenixRPA background received:",
            message
        );

        // Ignore messages that are not recorder events
        if (!message || message.type !== "RECORDER_EVENT") {
            return false;
        }

        // ----------------------------------------------------
        // Validate event
        // ----------------------------------------------------

        if (!message.event) {
            console.error(
                "PhoenixRPA: Missing event data"
            );

            sendResponse({
                success: false,
                error: "Missing event data"
            });

            return false;
        }

        console.log(
            "PhoenixRPA → Backend:",
            message.event
        );

        // ----------------------------------------------------
        // Send event to FastAPI
        // ----------------------------------------------------

        fetch(
            `${BACKEND_URL}/recorder/event`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(
                    message.event
                )
            }
        )
            .then(async (response) => {

                console.log(
                    "PhoenixRPA backend status:",
                    response.status
                );

                // Read response body
                let data;

                try {
                    data = await response.json();
                } catch (error) {
                    data = null;
                }

                // Backend returned an error
                if (!response.ok) {

                    throw new Error(
                        `Backend returned HTTP ${response.status}`
                    );
                }

                console.log(
                    "PhoenixRPA backend response:",
                    data
                );

                sendResponse({
                    success: true,
                    data: data
                });
            })

            .catch((error) => {

                console.error(
                    "PhoenixRPA backend error:",
                    error
                );

                sendResponse({
                    success: false,
                    error: error.message
                });
            });

        // IMPORTANT:
        // Keep the message channel open because
        // fetch() is asynchronous.
        return true;
    }
);