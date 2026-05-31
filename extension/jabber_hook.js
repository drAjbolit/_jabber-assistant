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
            ws.readyState === WebSocket.OPEN
        ) {

            ws.send(
                JSON.stringify({
                    type: "heartbeat",
                    ts: Date.now()
                })
            );
        }

    }, 1000);

    const seenMessages =
        new Set();

    function processMessageNode(
        textNode
    ) {

        const msg =
            textNode.closest(
                ".chat-msg"
            );

        if (!msg) {
            return;
        }

        const from =
            msg.dataset.from || "";

        /*
         * Игнорируем собственные
         * сообщения бота.
         */

        if (
            from ===
            "vova_gpt@jabber.ru"
        ) {

            return;
        }

        const msgId =
            msg.dataset.msgid;

        if (!msgId) {
            return;
        }

        if (
            seenMessages.has(
                msgId
            )
        ) {
            return;
        }

        seenMessages.add(
            msgId
        );

        const text =
            (
                textNode.innerText ||
                ""
            ).trim();

        if (!text) {
            return;
        }

        console.log(
            "NEW JABBER MESSAGE:",
            msgId
        );

        console.log(
            text
        );

        if (
            ws &&
            ws.readyState === WebSocket.OPEN
        ) {

            ws.send(
                JSON.stringify({
                    type:
                        "jabber_message",
                    msgid:
                        msgId,
                    from:
                        from,
                    text:
                        text
                })
            );

            console.log(
                "MESSAGE SENT TO PYTHON"
            );
        }
    }

    function processExistingHistory() {

        document
            .querySelectorAll(
                ".chat-msg"
            )
            .forEach(msg => {

                const msgId =
                    msg.dataset.msgid;

                if (msgId) {

                    seenMessages.add(
                        msgId
                    );
                }
            });

        console.log(
            "INITIAL HISTORY SKIPPED:",
            seenMessages.size
        );
    }

    function startObserver() {

        const observer =
            new MutationObserver(
                mutations => {

                    mutations.forEach(
                        mutation => {

                            mutation
                                .addedNodes
                                .forEach(
                                    node => {

                                        if (
                                            !node.querySelectorAll
                                        ) {
                                            return;
                                        }

                                        if (
                                            node.matches &&
                                            node.matches(
                                                ".chat-msg__text"
                                            )
                                        ) {

                                            processMessageNode(
                                                node
                                            );
                                        }

                                        node
                                            .querySelectorAll(
                                                ".chat-msg__text"
                                            )
                                            .forEach(
                                                processMessageNode
                                            );
                                    }
                                );
                        }
                    );
                }
            );

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
    }

    function waitForChatReady() {

        const msgs =
            document.querySelectorAll(
                ".chat-msg"
            );

        console.log(
            "CHAT CHECK:",
            msgs.length
        );

        if (
            msgs.length < 10
        ) {

            setTimeout(
                waitForChatReady,
                1000
            );

            return;
        }

        processExistingHistory();

        startObserver();
    }

    waitForChatReady();

})();