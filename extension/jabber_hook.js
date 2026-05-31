alert("JABBER HOOK LOADED");

(function () {

    console.log("JABBER HOOK START");

    if (window.__assistant_hook_installed) {
        return;
    }

    window.__assistant_hook_installed = true;

    console.log("HOOK INSTALLED");

    let ws = null;

    function connectWS() {

        try {

            ws = new WebSocket(
                "ws://127.0.0.1:8765"
            );

            ws.onopen = () => {

                console.log(
                    "ASSISTANT WS CONNECTED"
                );

                ws.send(
                    JSON.stringify({
                        type: "test",
                        text: "hello"
                    })
                );

                console.log(
                    "TEST SENT"
                );
            };

            ws.onclose = () => {

                console.log(
                    "ASSISTANT WS CLOSED"
                );

                setTimeout(
                    connectWS,
                    1000
                );
            };

            ws.onerror = (e) => {

                console.error(
                    "WS ERROR",
                    e
                );
            };

        } catch (e) {

            console.error(
                "WS CONNECT ERROR",
                e
            );

            setTimeout(
                connectWS,
                1000
            );
        }
    }

    connectWS();

    setInterval(() => {

        if (
            ws &&
            ws.readyState === 1
        ) {

            ws.send(
                JSON.stringify({
                    type: "heartbeat",
                    ts: Date.now()
                })
            );
        }

    }, 1000);

    const seen = new Set();

    function sendMessage(text) {

        if (!text) {
            return;
        }

        text = text.trim();

        if (!text) {
            return;
        }

        if (seen.has(text)) {
            return;
        }

        seen.add(text);

        console.log(
            "NEW JABBER MESSAGE:",
            text
        );

        if (
            ws &&
            ws.readyState === 1
        ) {

            ws.send(
                JSON.stringify({
                    type: "jabber_message",
                    text: text
                })
            );

            console.log(
                "MESSAGE SENT TO PYTHON"
            );
        }
    }

    function scanMessages() {

        document
            .querySelectorAll(
                ".chat-msg__text"
            )
            .forEach(el => {

                sendMessage(
                    el.innerText
                );
            });
    }

    scanMessages();

    const observer =
        new MutationObserver(() => {

            scanMessages();
        });

    observer.observe(
        document.body,
        {
            childList: true,
            subtree: true
        }
    );

    console.log(
        "DOM OBSERVER INSTALLED"
    );

})();