import requests
import os

URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/parse")
# PDF_PATH = os.getenv("TEST_PDF", "datasheet.pdf")

names = ["C2838500", "C26350", "C476817", "C86590"]
# check if there is already file:
done = False
for i in range(len(names)):
    if os.path.exists(names[i] + ".json"):
        with open(names[i] + ".json", "r") as f:
            with open("adjacency_" + str(i) + ".json", "w") as f2:
                f2.write(f.read())
        continue
    else:
        r = requests.post(URL + "?pdfUrl=https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/" + names[i] + ".pdf&part_name=" + names[i], timeout=300)
        print("Status:", r.status_code)
        body = r.json()
        structured = body.get("structured")
        with open("adjacency_" + str(i) + ".json", "w") as f:
            f.write(structured)
        with open(names[i] + ".json", "w") as f2:
            f2.write(structured)
        f.close()
        f2.close()
        break
    if i == len(names) - 1:
        done = True

if (done):
    print("All done")

