
"use client";

import { useState } from "react";

export default function InsightsPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<
    { role: string; content: string }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const prompts = [
    "Which species has the most sightings?",
    "Which camera IDs recorded the most activity?",
    "What patterns can you identify in hourly wildlife activity?",
    "What is the average detection confidence?",
    "What percentage of detections are unidentified?",
    "Suggest conservation actions based on these observations."
  ];

  async function askAI(text = question) {
    if (!text.trim() || loading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: text }
    ]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "AI request failed");
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Something went wrong."
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#07130f] text-white p-8">
      <div className="max-w-5xl mx-auto">
        <a href="/" className="text-emerald-400 text-sm">
          ← Back to dashboard
        </a>

        <p className="text-emerald-400 text-sm tracking-widest mt-8">
          AI-POWERED CONSERVATION
        </p>

        <h1 className="text-4xl font-bold mt-2">
          Insight Agent
        </h1>

        <p className="text-gray-400 mt-3 mb-8">
          Explore wildlife patterns and generate conservation insights
          using actual camera-trap pipeline data.
        </p>

        <div className="bg-[#11251c] border border-emerald-900 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-11 h-11 rounded-full bg-emerald-900 flex items-center justify-center">
              AI
            </div>

            <div>
              <h2 className="font-semibold">
                WildSight Intelligence
              </h2>
              <p className="text-xs text-emerald-400">
                Featherless AI Assistant
              </p>
            </div>
          </div>

          <div className="space-y-4 mb-6 max-h-[450px] overflow-y-auto">
            <div className="bg-[#07130f] rounded-xl p-5 text-gray-300">
              Hello! I'm your WildSight intelligence assistant.
              Ask me about species distribution, camera activity,
              detection confidence and conservation insights.
            </div>

            {messages.map((message, index) => (
              <div
                key={index}
                className={`rounded-xl p-4 whitespace-pre-wrap ${
                  message.role === "user"
                    ? "bg-emerald-900 ml-8"
                    : "bg-[#07130f] mr-8 text-gray-300"
                }`}
              >
                {message.content}
              </div>
            ))}

            {loading && (
              <div className="bg-[#07130f] rounded-xl p-4 text-emerald-300">
                Analyzing wildlife data...
              </div>
            )}
          </div>

          <p className="text-sm text-gray-400 mb-3">
            Suggested questions
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8">
            {prompts.map((prompt) => (
              <button
                key={prompt}
                onClick={() => askAI(prompt)}
                disabled={loading}
                className="text-left text-sm bg-[#193326] hover:bg-emerald-900 border border-emerald-900 rounded-lg p-4 disabled:opacity-50"
              >
                {prompt}
              </button>
            ))}
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              askAI();
            }}
            className="flex flex-col sm:flex-row gap-3"
          >
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about wildlife activity..."
              className="flex-1 bg-[#07130f] border border-emerald-900 rounded-lg px-4 py-3 outline-none focus:border-emerald-400"
            />

            <button
              type="submit"
              disabled={!question.trim() || loading}
              className="bg-emerald-700 hover:bg-emerald-600 disabled:opacity-40 px-6 py-3 rounded-lg font-semibold"
            >
              {loading ? "Thinking..." : "Ask AI →"}
            </button>
          </form>
        </div>

        <p className="text-gray-500 text-xs mt-4">
          AI-generated recommendations are suggestions and should
          be evaluated before conservation decisions.
        </p>
      </div>
    </main>
  );
}
