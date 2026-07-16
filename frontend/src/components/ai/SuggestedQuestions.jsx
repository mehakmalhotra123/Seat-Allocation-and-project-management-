import {
  MapPin,
  Briefcase,
  Building2,
  Users,
  BarChart3,
} from "lucide-react";

const questions = [
  {
    icon: <MapPin size={18} />,
    text: "Where is EMP0001 seated?",
  },
  {
    icon: <Briefcase size={18} />,
    text: "Which project is EMP0001 assigned to?",
  },
  {
    icon: <Building2 size={18} />,
    text: "Show available seats on Floor 3",
  },
  {
    icon: <Users size={18} />,
    text: "Who is sitting near EMP0001?",
  },
  {
    icon: <BarChart3 size={18} />,
    text: "How many seats are occupied for Indigo?",
  },
];

export default function SuggestedQuestions({
  sendMessage,
}) {
  return (
    <div className="bg-white rounded-xl shadow p-5">

      <h2 className="text-lg font-semibold mb-4">
        Suggested Questions
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">

        {questions.map((item, index) => (
          <button
            key={index}
            onClick={() => sendMessage(item.text)}
            className="flex items-center gap-3 border rounded-xl p-4 hover:bg-indigo-50 hover:border-indigo-400 transition-all duration-200 text-left"
          >
            <div className="text-indigo-600">
              {item.icon}
            </div>

            <span className="text-sm">
              {item.text}
            </span>
          </button>
        ))}

      </div>

    </div>
  );
}