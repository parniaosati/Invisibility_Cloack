# 🧙‍♂️ Invisibility Cloak Game (Harry Potter-Inspired)

Welcome to the **Invisibility Cloak Game**, a fun computer vision project inspired by the magical world of Harry Potter. This project uses Python and OpenCV to create the illusion of invisibility by detecting a colored cloak and replacing it with the background in real-time!

🔗 **Play it Online:** [https://parniaosati.github.io/cloak-backend/](https://parniaosati.github.io/cloak-backend/)

---

## 🎯 Purpose

This project was created purely for fun—as a way to explore the capabilities of **OpenCV** and **Python**, while also indulging my interest in the world of **Harry Potter**. 🧹✨

---

## 🛠️ How It Works

The program uses your webcam and performs the following steps:

1. **Background Capture:** Step out of the frame and click the "READY" button to capture a static background.
2. **Cloak Color Selection:** Choose a cloak color (red, green, or blue recommended).
3. **Invisibility Effect:** Wear a cloak of the selected color — it will magically disappear!

**Interface Includes:**
- 📷 Main video feed (with invisibility effect)
- 🪞 Original preview window
- 🧭 Assistant UI to guide you through setup

---

## 🧪 Technologies Used

- **Python 3**
- **OpenCV**
- **NumPy**

Install dependencies using:

```bash
pip install opencv-python numpy
```
## 🚀 How to Run Locally

1. Clone the repository or download the script.

2. Ensure your webcam is connected.

3. Run the script:

```bash
python invisibility_cloak.py
```
4. Follow the instructions on the "Cloak Assistant" window:

  - Step out of the frame and click "READY".

  - Choose a cloak color.

  - Step back in with a cloak of the selected color and watch the magic happen!

## 🧠 Behind the Scenes

The cloak detection works by:

  - Converting the video frame to HSV color space.

  - Applying color thresholding to detect the selected cloak color.

  - Creating a mask and blending background and current frame to hide the cloak.

HSV ranges for various cloak colors are pre-defined, and morphological operations are applied to improve mask quality.

## ❗ Notes

  - For best results, use a **bright, solid-colored cloak**.

  - Avoid backgrounds or clothing that match the cloak color.

  - Works best in well-lit environments.

## 📎 Online Version

You can play the game directly in your browser using this link:

🔗 https://parniaosati.github.io/cloak-backend/

## 🙌 Acknowledgments

Special thanks to the **OpenCV community** for making computer vision so accessible and fun. Inspired by the magic of **Harry Potter**!
