import React, { useState } from "react";
import axios from "axios";

function App() {
  const [image, setImage] = useState(null);
  const [dropdownValue, setDropdownValue] = useState("");
  const [response, setResponse] = useState(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleDropdownChange = (e) => {
    setDropdownValue(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!image || !dropdownValue) {
      alert("Please select an image and a dropdown value.");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("plant", dropdownValue);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      console.log(response)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error("Error uploading data:", error);
      alert("Failed to upload data.");
    }
  };

  return (
    <div>
      <h1>Image and Dropdown Submission</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Upload Image: </label>
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </div>
        <div>
          <label>Select Option: </label>
          <select value={dropdownValue} onChange={handleDropdownChange}>
            <option value="">--Choose an option--</option>
            <option value="apple">apple</option>
            <option value="cherry">cherry</option>
            <option value="peach">peach</option>
            <option value="pepper">pepper</option>
            <option value="potato">potato</option>
            <option value="strawberry">strawberry</option>
          </select>
        </div>
        <button type="submit">Submit</button>
      </form>

      {response && (
        <div>
          <h2>Server Response:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App
