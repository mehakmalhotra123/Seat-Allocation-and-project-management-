import { useState } from "react";
import ChatMessage from "../components/ai/ChatMessage";
import ChatInput from "../components/ai/ChatInput";
import SuggestedQuestions from "../components/ai/SuggestedQuestions";
import TypingIndicator from "../components/ai/TypingIndicator";
import api from "../api/api";

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "👋 Hello! I'm Ethara AI Assistant.\n\nI can help you with:\n\n• Employee Seat\n• Project Assignment\n• Available Seats\n• Floor Utilization\n• Nearby Employees",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const res = await api.post("/ai/query", {
        query: text,
      });

      const botMessage = {
        id: Date.now() + 1,
        type: "bot",
        text: res.data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const botMessage = {
        id: Date.now() + 2,
        type: "bot",
        text:
          err.response?.data?.detail ||
          "Unable to process your request.",
      };

      setMessages((prev) => [...prev, botMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="h-full flex flex-col">

      <div className="mb-6">

        <h1 className="text-4xl font-bold">
          AI Assistant
        </h1>

        <p className="text-gray-500 mt-2">
          Ask anything about employees,
          projects and seat allocation.
        </p>

      </div>

      <SuggestedQuestions sendMessage={sendMessage} />

      <div
        className="flex-1 bg-white rounded-xl shadow mt-5 p-5 overflow-y-auto"
        style={{ minHeight: "500px" }}
      >
        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            message={msg}
          />
        ))}

        {loading && <TypingIndicator />}
      </div>

      <ChatInput sendMessage={sendMessage} />

    </div>
  );
}