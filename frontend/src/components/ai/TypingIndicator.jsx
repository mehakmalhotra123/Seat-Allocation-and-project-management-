import { Bot } from "lucide-react";

export default function TypingIndicator() {
  return (
    <div className="flex items-start mb-5">

      <div className="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center mr-3">
        <Bot size={20} />
      </div>

      <div className="bg-gray-100 rounded-2xl rounded-tl-none px-5 py-4 shadow-sm">

        <p className="text-sm text-gray-500 mb-3">
          Ethara AI is thinking...
        </p>

        <div className="flex items-center gap-2">

          <span
            className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          />

          <span
            className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
            style={{ animationDelay: "200ms" }}
          />

          <span
            className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
            style={{ animationDelay: "400ms" }}
          />

        </div>

      </div>

    </div>
  );
}