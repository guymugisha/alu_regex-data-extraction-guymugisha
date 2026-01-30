import re
import json
import os


# =========================
# Read input file
# =========================
def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error: {file_path} not found or unreadable.")
        print(e)
        return ""


# =========================
# Extract data using regex
# =========================
def extract_data(text: str) -> dict:
    results = {
        "emails": [],
        "urls": [],
        "phoneNumbers": [],
        "currencyAmounts": [],
        "creditCards": [],
        "timestamps": [],
    }

    # Emails
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    email_matches = re.findall(email_regex, text)
    results["emails"] = [
        (local[0] + "***" + local[-1] + "@" + domain if len(local) > 1 else local + "***@" + domain)
        for email in email_matches if ".." not in email
        for local, domain in [email.split("@")]
    ]

    # URLs
    url_regex = r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    url_matches = re.findall(url_regex, text)
    results["urls"] = [
        url for url in url_matches
        if "<script>" not in url.lower() and "javascript:" not in url.lower()
    ]

    # Phone numbers
    phone_regex = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    results["phoneNumbers"] = re.findall(phone_regex, text)

    # Currency amounts
    currency_regex = r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
    results["currencyAmounts"] = re.findall(currency_regex, text)

    # Credit cards
    cc_regex = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
    cc_matches = re.findall(cc_regex, text)
    results["creditCards"] = [
        "****-****-****-" + cc.replace("-", "").replace(" ", "")[-4:]
        for cc in cc_matches
        if len(cc.replace("-", "").replace(" ", "")) == 16
    ]

    # Timestamps
    time_regex = r"\b(?:[01]?\d|2[0-3]):[0-5]\d(?:\s?[APMapm]{2})?\b"
    results["timestamps"] = re.findall(time_regex, text)

    return results


# =========================
# Save JSON (OPTION 1)
# =========================
def save_json(extracted_data, filename="output.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)

                # If file contains a dict, convert it to a list
                if not isinstance(data, list):
                    data = [data]

            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(extracted_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================
# Main program
# =========================
def main():
    input_text = read_file("input.txt")
    if not input_text:
        return

    extracted_data = extract_data(input_text)

    # Print extracted data
    print(json.dumps(extracted_data, indent=4))

    # Save to JSON file
    save_json(extracted_data)

    print("Data successfully saved to output.json")


if __name__ == "__main__":
    main()
