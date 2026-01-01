import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard",
      },
    ],
  }),
})

function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl">Welcome 👋</h1>
      <p className="text-muted-foreground">Dashboard coming soon...</p>
    </div>
  )
}
