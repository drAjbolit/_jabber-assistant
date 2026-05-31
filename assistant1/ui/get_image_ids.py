def get_image_ids(page):

    return set(
        page.evaluate(
            '''
            () => {
                return Array.from(document.querySelectorAll("img"))
                .map(x => x.src)
                .filter(x => x.includes("backend-api/estuary/content?id="))
                .map(x => {
                    const m = x.match(/id=([^&]+)/);
                    return m ? m[1] : null;
                })
                .filter(x => x);
            }
            '''
        )
    )
