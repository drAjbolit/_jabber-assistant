import base64

def save_last_generated_image(page, output_path):

    result = page.evaluate(
        '''
        async () => {

            const imgs = Array.from(
                document.querySelectorAll("img")
            );

            const target = imgs
                .filter(
                    x => x.src.includes(
                        "backend-api/estuary"
                    )
                )
                .sort(
                    (a,b) =>
                    (b.width*b.height)
                    -
                    (a.width*a.height)
                )[0];

            if (!target)
                return null;

            const response =
                await fetch(target.src);

            const blob =
                await response.blob();

            const reader =
                new FileReader();

            return await new Promise(
                resolve => {

                    reader.onload =
                        () => resolve(
                            reader.result
                        );

                    reader.readAsDataURL(
                        blob
                    );
                }
            );
        }
        '''
    )

    if not result:
        return False

    pos = result.find("base64,")

    if pos == -1:
        return False

    data = result[pos + 7:]

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(data))

    return True
