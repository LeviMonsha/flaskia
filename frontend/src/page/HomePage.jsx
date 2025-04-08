import React from "react";
import { useLocation } from "react-router-dom";

function HomePage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const username = params.get("username");
  const title = params.get("title");

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4">{title}</h1>
        <p className="text-gray-700">Hello, {username}!</p>
      </div>
    </div>
  );
}

export default HomePage;
