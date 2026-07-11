import React from "react";
import { useAuth } from "@/features/auth/AuthProvider";
import { useDashboardData } from "@/features/dashboard/useDashboardData";
import {
  CheckCircle,
  HelpCircle,
  Trophy,
  Clock,
  ArrowRight,
  Play,
  BarChart2
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

interface TopicMasteryData {
  name: string;
  score: number;
}

interface RecentInterviewData {
  role: string;
  category: string;
  questions: number;
  date: string;
  score: number;
}

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const {
    stats,
    performance,
    topicMastery,
    recommended,
    recentInterviews,
    isLoading
  } = useDashboardData();

  const firstName = user?.user_metadata?.full_name?.split(" ")[0] || user?.email?.split("@")[0] || "there";

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-24 bg-gray-200 rounded-lg w-full"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-80 bg-gray-200 rounded-lg"></div>
          <div className="h-80 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Welcome Section */}
      <section className="bg-white p-6 rounded-xl border border-border shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Welcome back, {firstName}</h1>
          <p className="text-muted-foreground mt-1">Continue building your interview skills with focused AI-guided practice.</p>
        </div>
        <div className="flex flex-col sm:flex-row gap-3">
          <button className="bg-secondary text-foreground hover:bg-secondary/80 px-4 py-2 rounded-md font-medium transition-colors border border-border">
            Practice One Question
          </button>
          <button className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md font-medium flex items-center justify-center gap-2 transition-colors">
            Start Mock Interview
            <ArrowRight size={18} />
          </button>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Interviews completed", value: stats?.interviewsCompleted || 0, icon: CheckCircle, color: "text-blue-500" },
          { label: "Questions answered", value: stats?.questionsAnswered || 0, icon: HelpCircle, color: "text-indigo-500" },
          { label: "Average score", value: `${stats?.averageScore || 0}%`, icon: Trophy, color: "text-amber-500" },
          { label: "Total practice time", value: `${stats?.practiceTimeMinutes || 0}m`, icon: Clock, color: "text-emerald-500" },
        ].map((stat, i) => (
          <div key={i} className="bg-white p-5 rounded-xl border border-border shadow-sm flex items-start justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{stat.value}</h3>
            </div>
            <div className={`p-2 rounded-md bg-secondary ${stat.color}`}>
              <stat.icon size={20} />
            </div>
          </div>
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Performance Chart */}
        <section className="bg-white p-6 rounded-xl border border-border shadow-sm lg:col-span-2">
          <h2 className="text-lg font-bold text-foreground mb-4">Recent performance</h2>
          {performance && performance.length > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={performance}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                  <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-center bg-secondary/30 rounded-lg border border-dashed border-border">
              <BarChart2 className="h-10 w-10 text-muted-foreground mb-2" />
              <h3 className="text-sm font-medium text-foreground">No session data yet</h3>
              <p className="text-xs text-muted-foreground mt-1 max-w-[200px]">Complete your first mock interview to see your performance trends.</p>
            </div>
          )}
        </section>

        {/* Topic Mastery */}
        <section className="bg-white p-6 rounded-xl border border-border shadow-sm">
          <h2 className="text-lg font-bold text-foreground mb-4">Topic mastery</h2>
          {topicMastery && topicMastery.length > 0 ? (
            <div className="space-y-4">
              {(topicMastery as TopicMasteryData[]).map((topic, i: number) => (
                <div key={i}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">{topic.name}</span>
                    <span className="text-muted-foreground">{topic.score}%</span>
                  </div>
                  <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary rounded-full"
                      style={{ width: `${topic.score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
             <div className="h-48 flex flex-col items-center justify-center text-center bg-secondary/30 rounded-lg border border-dashed border-border">
               <Trophy className="h-8 w-8 text-muted-foreground mb-2" />
               <p className="text-sm text-muted-foreground">Practice questions to build topic mastery.</p>
             </div>
          )}
        </section>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recommended Practice */}
        <section className="bg-white p-6 rounded-xl border border-border shadow-sm">
          <h2 className="text-lg font-bold text-foreground mb-4">Recommended practice</h2>
          {recommended ? (
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-foreground">{recommended.category}</h3>
                <p className="text-sm text-muted-foreground mt-1">{recommended.reason}</p>
              </div>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span className="bg-secondary px-2 py-1 rounded-md">{recommended.difficulty}</span>
                <span>~{recommended.duration} min</span>
              </div>
              <button className="w-full bg-secondary text-foreground hover:bg-secondary/80 py-2 rounded-md font-medium flex justify-center items-center gap-2 transition-colors border border-border">
                <Play size={16} /> Start Drill
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center text-center h-32 bg-secondary/30 rounded-lg border border-dashed border-border">
              <p className="text-sm text-muted-foreground px-4">Complete an interview session to receive personalized recommendations.</p>
            </div>
          )}
        </section>

        {/* Recent Interviews */}
        <section className="bg-white p-6 rounded-xl border border-border shadow-sm lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-bold text-foreground">Recent interviews</h2>
            <button className="text-sm text-primary hover:underline font-medium">View all</button>
          </div>

          {recentInterviews && recentInterviews.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-muted-foreground uppercase bg-secondary/50 rounded-md">
                  <tr>
                    <th className="px-4 py-3 rounded-l-md font-medium">Role & Category</th>
                    <th className="px-4 py-3 font-medium">Date</th>
                    <th className="px-4 py-3 font-medium">Score</th>
                    <th className="px-4 py-3 rounded-r-md text-right font-medium">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {(recentInterviews as RecentInterviewData[]).map((interview, i: number) => (
                    <tr key={i} className="border-b border-border last:border-0 hover:bg-secondary/30">
                      <td className="px-4 py-3">
                        <div className="font-medium text-foreground">{interview.role}</div>
                        <div className="text-muted-foreground text-xs">{interview.category} • {interview.questions} Qs</div>
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">{interview.date}</td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {interview.score}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button className="text-primary hover:text-primary/80 font-medium text-sm">View report</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center text-center py-8 bg-secondary/30 rounded-lg border border-dashed border-border">
              <p className="text-sm text-muted-foreground mb-4">You haven't completed any interviews yet.</p>
              <button className="bg-white text-foreground hover:bg-secondary border border-border px-4 py-2 rounded-md font-medium transition-colors shadow-sm">
                Start your first interview
              </button>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
