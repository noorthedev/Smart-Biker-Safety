# 🚨 RideGuard - Smart Biker Safety & Incident Reporting

**RideGuard** is a Streamlit web application designed to allow users to report reckless driving incidents involving tankers or other vehicles, view reported incidents on a live map, and analyze data through an admin dashboard.

## 🛠️ Features

- 🔐 User Authentication (Register & Login)
- 🚴 Report Incidents with Media Upload and Geo-location
- 🗺️ View All Incidents on a Live Map (Folium)
- 📄 View All Reports in Tabular Form
- 📊 Admin Dashboard with Top Offenders
- 💡 Safety Tips for Bikers
- 💬 Submit User Feedback

## 🚀 Getting Started

### Prerequisites

- Python 3.8+

 🧠 Object-Oriented Design
The RideGuard application implements the 4 fundamental principles of Object-Oriented Programming (OOP):

1. Encapsulation
- Classes jaise User, Incident, aur Feedback mein data aur unke related methods ko encapsulate kiya gaya hai.
- Private variables aur methods ka istemal karke data ko unauthorized access se mehfooz rakha gaya hai.

2. Inheritance
- AdminUser class ko User class se inherit kiya gaya hai, jisse admin users ko additional privileges milte hain.
- Is se code reuse hota hai aur hierarchy create hoti hai.

3. Polymorphism
- display() method ko Incident aur Feedback classes mein alag tareeqon se implement kiya gaya hai.
- Is se ek hi method ka different contexts mein different behavior hota hai.

4. Abstraction
- AuthService aur MapService jaise services mein internal complexities ko chhupa kar sirf essential features expose kiye gaye hain.
- Is se user ko sirf zaroori information milti hai, jo system ko simplify karti hai.
