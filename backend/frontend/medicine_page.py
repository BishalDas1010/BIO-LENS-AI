from pathlib import Path

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


# ---------------- Helpers ----------------
def _lookup_medicine(name: str, question: str = "") -> str:
    """Call /medicine and return the reply text (or an error string)."""
    try:
        r = requests.post(
            f"{API_URL}/medicine",
            json={"medicine_name": name, "question": question},
            timeout=120,
        )
        if r.status_code == 200:
            return r.json()["reply"]
        return f"⚠️ API error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot reach backend. Is FastAPI running?"
    except Exception as e:
        return f"⚠️ {e}"


def _scan_prescription(image_bytes: bytes, filename: str) -> dict:
    """Send the image to /medicine/scan and return extracted medicine names."""
    files = {"file": (filename, image_bytes)}
    try:
        r = requests.post(f"{API_URL}/medicine/scan", files=files, timeout=120)
        if r.status_code == 200:
            return r.json()
        return {"error": f"API error {r.status_code}: {r.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot reach backend."}
    except Exception as e:
        return {"error": str(e)}


# ---------------- Page ----------------
def medicine_page():
    st.markdown(
        """
        <style>
        div[data-testid="stSegmentedControl"] button {
            border-radius: 10px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
   
    st.title("Medicine Information")
    st.caption(
        "Type a medicine name, or upload / take a photo of your prescription. "
        "Data is retrieved live from the web with citations."
    )

    col1, col2 = st.columns([2, 3])

    with col1:
        with st.container(border=True):
            medicine = ""
            question = ""
            search_clicked = False
            extracted_meds: list[str] = []

            # 🔀 Toggle: Type vs Camera
            mode = st.segmented_control(
                "Input mode",
                options=["📝 Type it", "📷 Camera"],
                default="📝 Type it",
                label_visibility="collapsed",
                key="med_input_mode",
            ) or "📝 Type it"

            # --- TEXT MODE ---
            if mode == "📝 Type it":
                st.subheader("🔍 Search Medicine")
                medicine = st.text_input(
                    "Medicine Name",
                    placeholder="e.g. Ibuprofen, Metformin, Amoxicillin",
                )
                question = st.text_area(
                    "Specific Question (optional)",
                    placeholder="e.g. What are the side effects? Can I take it with food?",
                    height=80,
                )
                search_clicked = st.button("🔎 Search", use_container_width=True)

            # --- CAMERA / UPLOAD MODE ---
            else:
                st.subheader("Prescription Photo")

                img_source = st.segmented_control(
                    "Image source",
                    options=[" Upload", "📸 Camera"],
                    default=" Upload",
                    label_visibility="collapsed",
                    key="med_img_source",
                ) or " Upload"

                image_file = None
                if img_source == "📁 Upload":
                    image_file = st.file_uploader(
                        "Upload a prescription image",
                        type=["png", "jpg", "jpeg", "webp"],
                    )
                else:
                    image_file = st.camera_input("Take a photo of your prescription")

                if image_file is not None:
                    st.image(image_file, caption="Preview", use_container_width=True)

                    if st.button("🧠 Extract Medicines", use_container_width=True):
                        with st.spinner("Reading prescription..."):
                            data = _scan_prescription(
                                image_file.getvalue(), image_file.name
                            )

                        if "error" in data:
                            st.error(data["error"])
                        else:
                            extracted_meds = data.get("medicines", [])
                            if not extracted_meds:
                                st.warning("No medicine names found in the image.")
                            else:
                                st.success(
                                    f"Found {len(extracted_meds)} medicine(s):"
                                )
                                st.session_state["scanned_meds"] = extracted_meds

                # show any meds previously extracted in this session
                if not extracted_meds and st.session_state.get("scanned_meds"):
                    extracted_meds = st.session_state["scanned_meds"]

                if extracted_meds:
                    st.markdown("**Detected medicines:**")
                    picked = st.multiselect(
                        "Choose one to look up:",
                        options=extracted_meds,
                        default=extracted_meds[:1],
                        key="picked_med",
                    )
                    question = st.text_area(
                        "Specific Question (optional)",
                        placeholder="e.g. What are the side effects?",
                        height=80,
                        key="q_photo",
                    )
                    if st.button("🔎 Look up", use_container_width=True):
                        if picked:
                            medicine = picked[0]
                            search_clicked = True
                        else:
                            st.warning("Pick a medicine first.")

    # ---------------- RIGHT: RESULTS ----------------
    with col2:
        with st.container(border=True):
            st.subheader("📋 Results")

            if search_clicked and medicine:
                with st.spinner("Searching medical databases and the web..."):
                    reply = _lookup_medicine(medicine, question or "")
                st.markdown(f"###  {medicine}")
                st.markdown(reply)

            elif search_clicked and not medicine:
                st.warning("Please enter or select a medicine name.")
            else:
                st.info("Enter a medicine name or scan a prescription to begin.")