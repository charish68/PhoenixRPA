const status = document.getElementById("status");


// ============================================================
// START RECORDING
// ============================================================

document
    .getElementById("start")
    .addEventListener("click", async () => {

        try {

            status.innerText = "Starting recorder...";

            const response = await fetch(
                "http://127.0.0.1:8000/recorder/start",
                {
                    method: "POST"
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Backend returned ${response.status}`
                );
            }

            const data = await response.json();

            console.log(
                "PhoenixRPA Start:",
                data
            );

            status.innerText = data.message;

        } catch (error) {

            console.error(
                "PhoenixRPA Start Error:",
                error
            );

            status.innerText =
                "Failed to start recording";
        }
    });


// ============================================================
// STOP RECORDING
// ============================================================

document
    .getElementById("stop")
    .addEventListener("click", async () => {

        try {

            status.innerText = "Stopping recorder...";

            const response = await fetch(
                "http://127.0.0.1:8000/recorder/stop",
                {
                    method: "POST"
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Backend returned ${response.status}`
                );
            }

            const data = await response.json();

            console.log(
                "PhoenixRPA Stop:",
                data
            );

            status.innerText = data.message;

        } catch (error) {

            console.error(
                "PhoenixRPA Stop Error:",
                error
            );

            status.innerText =
                "Failed to stop recording";
        }
    });