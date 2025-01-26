import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import FoundItems from "./pages/FoundItems";
import LostItems from "./pages/LostItems";
import Profile from "./pages/Profile";
import { AuthProvider } from "./context/AuthContext";
import { type IItem, type ICreateItem } from "./api/types";
import { httpClient } from "./api/client";
import { ItemTypes } from "./api/enums";

function App() {
  const [items, setItems] = useState<IItem[]>([]);

  useEffect(() => {
    httpClient.getAllItems().then((res) => setItems(res.data!));
  }, []);

  const handleAddItem = (item: ICreateItem) => {
    httpClient.createItem(item).then((res) => {
      if (!res.error) {
        httpClient.getAllItems().then(($res) => setItems($res.data!));
      }
    });
  };

  return (
    <Router>
      <Header onAddItem={handleAddItem} />
      <div className="container">
        <Routes>
          <Route
            path="/found"
            element={
              <FoundItems
                items={items.filter((item) => item.type === ItemTypes.FOUND)}
              />
            }
          />
          <Route
            path="/lost"
            element={
              <LostItems
                items={items.filter((item) => item.type === ItemTypes.LOST)}
              />
            }
          />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </Router>
  );
}

function AppWrapper() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}
export default AppWrapper;
