import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import st_folium

# -------------------- Models --------------------
class Report:
    def __init__(self, plate, location, description, media, lat, lon):
        self.plate = plate
        self.location = location
        self.description = description
        self.media = media
        self.lat = lat
        self.lon = lon
        self.timestamp = datetime.datetime.now()

    def to_dict(self):
        return {
            "plate": self.plate,
            "location": self.location,
            "description": self.description,
            "media": self.media,
            "lat": self.lat,
            "lon": self.lon,
            "timestamp": self.timestamp
        }

# -------------------- Managers --------------------
class ReportManager:
    def __init__(self):
        if "reports" not in st.session_state:
            st.session_state["reports"] = []

    def add_report(self, report: Report):
        st.session_state["reports"].append(report.to_dict())

    def get_all_reports(self):
        return st.session_state["reports"]

    def get_top_offenders(self, top_n=5):
        df = pd.DataFrame(self.get_all_reports())
        return df['plate'].value_counts().head(top_n) if not df.empty else pd.Series()

    def get_report_df(self):
        return pd.DataFrame(self.get_all_reports())

class AuthManager:
    def __init__(self):
        if "users" not in st.session_state:
            st.session_state["users"] = {"admin": "admin123"}  # default user
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
        if "current_user" not in st.session_state:
            st.session_state["current_user"] = ""

    def register(self, username, password):
        if username in st.session_state["users"]:
            return False
        st.session_state["users"][username] = password
        return True

    def login(self, username, password):
        if st.session_state["users"].get(username) == password:
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            return True
        return False

    def logout(self):
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = ""

# -------------------- App --------------------
class RideGuardApp:
    def __init__(self):
        self.manager = ReportManager()
        self.auth = AuthManager()

    def run(self):
        st.set_page_config(page_title="RideGuard", layout="wide")
        st.title("🚨 RideGuard - Smart Biker Safety & Incident Reporting")

        menu = st.sidebar.radio("Navigate", ["🔐 Login", "📝 Register", "🚴 Report Incident","📄 View Reports" ,"🗺️ View Map", "📊 Admin Dashboard", "💡 Safety Tips", "💬 Feedback"])

        if menu == "🔐 Login":
            self.login()
        elif menu == "📝 Register":
            self.register()
        elif menu == "🚴 Report Incident":
            if st.session_state["logged_in"]:
                self.report_incident()
            else:
                st.warning("Please login to report incidents.")
        elif menu == "🗺️ View Map":
            self.view_map()
        elif menu == "📊 Admin Dashboard":
            if st.session_state["current_user"] == "admin":
                self.admin_dashboard()
            else:
                st.warning("Admin access only.")
        elif menu == "💡 Safety Tips":
            self.safety_tips()
        elif menu == "💬 Feedback":
            self.feedback_form()

        if menu == "📄 View Reports":
            self.view_reports()    

        self.footer()

    def login(self):
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if self.auth.login(username, password):
                st.success("Logged in successfully as " + username)
            else:
                st.error("Invalid username or password")


    def register(self):
        st.subheader("📝 Register")
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Register"):
            if self.auth.register(username, password):
                st.success("Registered successfully! Please log in.")
            else:
                st.error("Username already exists")

    def report_incident(self):
        st.header("🚨 Report Reckless Tanker / Vehicle")
        with st.form("report_form"):
            plate = st.text_input("Vehicle Plate Number (e.g., LEA-1234)")
            location = st.text_input("Location (e.g., Korangi, Karachi)")
            description = st.text_area("Incident Description")
            uploaded_file = st.file_uploader("Upload Photo or Video", type=["jpg", "jpeg", "png", "mp4"])
            lat = st.number_input("Latitude", value=24.8607)
            lon = st.number_input("Longitude", value=67.0011)
            submit = st.form_submit_button("Submit Report")

        if submit:
            media_name = uploaded_file.name if uploaded_file else "N/A"
            report = Report(plate, location, description, media_name, lat, lon)
            self.manager.add_report(report)
            st.success("✅ Report submitted successfully!")


    def view_map(self):
        st.header("📍 Live Incident Map")
        m = folium.Map(location=[24.8607, 67.0011], zoom_start=11)
        for r in self.manager.get_all_reports():
            folium.Marker(
                location=[r['lat'], r['lon']],
                popup=f"{r['plate']} - {r['location']}<br>{r['description']}",
                icon=folium.Icon(color="red", icon="exclamation-triangle", prefix='fa')
            ).add_to(m)
        st_folium(m, width=800)

    def admin_dashboard(self):
        st.header("📋 Admin Dashboard: Incident Reports")
        reports_df = self.manager.get_report_df()
        if not reports_df.empty:
            st.dataframe(reports_df[['plate', 'location', 'timestamp', 'description']])
            st.subheader("🚨 Top Reported Plates")
            st.bar_chart(self.manager.get_top_offenders())
        else:
            st.info("No reports yet.")


    def view_reports(self):
        st.subheader("📊 RideGuard Report Summary")
        df = self.manager.get_report_df()

        if df.empty:
            st.warning("No reports submitted yet.")
        else:
            st.metric("📋 Total Reports", len(df))
            st.metric("🚛 Unique Vehicles Reported", df['plate'].nunique())
            st.dataframe(df)

            st.markdown("### 🔍 Most Common Violations")
            st.bar_chart(df['description'].value_counts())

    def safety_tips(self):
        st.header("💡 Accident Prevention Tips")
        st.markdown("""
        - ✅ Always wear a helmet and safety gear.
        - 🚦 Obey all traffic signals and speed limits.
        - 🔍 Stay alert and avoid distractions while riding.
        - 🌧️ Avoid speeding in rainy or poor visibility conditions.
        - 🔧 Regularly maintain your bike to avoid failures.
        - 🚗 Maintain a safe distance from tankers and heavy vehicles.
        """)

    def feedback_form(self):
        st.header("💬 User Feedback")
        with st.form("feedback_form"):
            name = st.text_input("Your Name")
            feedback = st.text_area("Your Feedback")
            submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success("Thank you for your feedback!")

    def footer(self):
        st.markdown("""
        <hr>
        <center>
        RideGuard - Revolutionizing Rider Safety | Crafted with ❤️ by Anum Rajput 
        </center>
        """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    app = RideGuardApp()
    app.run()
