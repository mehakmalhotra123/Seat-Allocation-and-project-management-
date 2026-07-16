import { Bot, User } from "lucide-react";

export default function ChatMessage({ message }) {
  const isBot = message.type === "bot";

  return (
    <div
      className={`flex mb-5 ${
        isBot ? "justify-start" : "justify-end"
      }`}
    >
      {isBot && (
        <div className="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center mr-3">
          <Bot size={20} />
        </div>
      )}

      <div
        className={`max-w-[75%] rounded-2xl px-5 py-4 whitespace-pre-wrap shadow-sm ${
          isBot
            ? "bg-gray-100 text-gray-800 rounded-tl-none"
            : "bg-indigo-600 text-white rounded-tr-none"
        }`}
      >
        <p className="text-sm leading-7">{message.text}</p>
      </div>

      {!isBot && (
        <div className="w-10 h-10 rounded-full bg-gray-800 text-white flex items-center justify-center ml-3">
          <User size={20} />
        </div>
      )}
    </div>
  );
}