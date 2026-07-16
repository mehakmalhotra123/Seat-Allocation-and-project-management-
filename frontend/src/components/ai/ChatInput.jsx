import { useState } from "react";
import { SendHorizontal } from "lucide-react";

export default function ChatInput({ sendMessage }) {
  const [message, setMessage] = useState("");

  const handleSubmit = () => {
    if (!message.trim()) return;

    sendMessage(message);
    setMessage("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="bg-white rounded-xl shadow mt-5 p-4">
      <div className="flex items-center gap-3">

        <textarea
          rows={1}
          placeholder="Ask something like 'Where is EMP0001 seated?'"
          className="flex-1 border rounded-xl px-4 py-3 resize-none outline-none focus:ring-2 focus:ring-indigo-500"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          onClick={handleSubmit}
          className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-xl transition duration-200"
        >
          <SendHorizontal size={22} />
        </button>

      </div>

      <div className="mt-2 text-xs text-gray-500">
        Press <strong>Enter</strong> to send • <strong>Shift + Enter</strong> for a new line.
      </div>
    </div>
  );
}