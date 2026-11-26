from rest_framework.views import exception_handler as default_exception_handler

_FIELD_LABELS = {
    "addressLine1": "House no. / address line 1",
    "addressLine2": "Address line 2",
    "postalCode": "PIN code",
    "fullName": "Full name",
    "offerPercentage": "Offer percentage",
    "categoryId": "Category",
}


def _humanize_field(name):
    if name in _FIELD_LABELS:
        return _FIELD_LABELS[name]
    return name.replace("_", " ").capitalize()


def _extract_error_messages(data, prefix=""):
    messages = []
    if isinstance(data, dict):
        for key, value in data.items():
            label = "" if key in ("non_field_errors", "detail") else _humanize_field(key)
            next_prefix = label if not prefix else (f"{prefix} {label}" if label else prefix)
            messages.extend(_extract_error_messages(value, next_prefix))
    elif isinstance(data, list):
        for item in data:
            messages.extend(_extract_error_messages(item, prefix))
    elif data is not None:
        text = str(data).strip()
        if text:
            messages.append(f"{prefix}: {text}" if prefix else text)
    return messages


def exception_handler(exc, context):
    response = default_exception_handler(exc, context)
    if response is None:
        return response
    if isinstance(response.data, dict) and "detail" in response.data:
        response.data = {"error": str(response.data["detail"])}
    else:
        raw_details = response.data
        messages = _extract_error_messages(raw_details)
        summary = " ".join(messages) if messages else "Please check the submitted information."
        response.data = {"error": summary, "details": raw_details}
    return response
