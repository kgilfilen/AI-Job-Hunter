import { useEffect, useState } from "react";

type ApplicationAttention = {
  application_id: number;
  job_id: number;
  status: string;
  next_action: string | null;
  follow_up_at: string | null;
  job_title: string | null;
  company: string | null;
};

type TrackedApplication = {
  application_id: number;
  job_id: number;
  status: string;
  job_title: string | null;
  company: string | null;
};

type ActivityEvent = {
  event_id: number;
  application_id: number;
  event_type: string;
  occurred_at: string;
  notes: string | null;
  job_id: number | null;
  job_title: string | null;
  company: string | null;
};

type ActivityForm = {
  application_id: string;
  event_type: string;
  notes: string;
};

function App() {
  const [applications, setApplications] = useState<ApplicationAttention[]>([]);

  const [trackedApplications, setTrackedApplications] = useState<
    TrackedApplication[]
  >([]);

  const [activityTypes, setActivityTypes] = useState<string[]>([]);

  const [activity, setActivity] = useState<ActivityEvent[]>([]);

  const [error, setError] = useState<string | null>(null);

  const [activityForm, setActivityForm] = useState<ActivityForm>({
    application_id: "",
    event_type: "",
    notes: "",
  });

  const [submitMessage, setSubmitMessage] = useState<string | null>(null);

  function loadRecentActivity() {
    fetch("http://127.0.0.1:8000/activity/today")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load recent activity");
        }

        return response.json();
      })
      .then((data) => {
        setActivity(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }

  function submitActivity(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    fetch("http://127.0.0.1:8000/activity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        application_id: Number(activityForm.application_id),
        event_type: activityForm.event_type,
        notes: activityForm.notes || null,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to record activity");
        }

        return response.json();
      })
      .then(() => {
        setSubmitMessage("Activity recorded.");

        setActivityForm({
          application_id: "",
          event_type: "",
          notes: "",
        });

        loadRecentActivity();
      })
      .catch((err) => {
        setSubmitMessage(err.message);
      });
  }

  useEffect(() => {
    fetch("http://127.0.0.1:8000/applications/needs-attention")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load applications");
        }

        return response.json();
      })
      .then((data) => {
        setApplications(data);
      })
      .catch((err) => {
        setError(err.message);
      });

    loadRecentActivity();

    fetch("http://127.0.0.1:8000/applications")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load tracked applications");
        }

        return response.json();
      })
      .then((data) => {
        setTrackedApplications(data);
      })
      .catch((err) => {
        setError(err.message);
      });

    fetch("http://127.0.0.1:8000/activity-types")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load activity types");
        }

        return response.json();
      })
      .then((data) => {
        setActivityTypes(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  return (
    <main>
      <h1>AI Career Manager</h1>

      <h2>Needs Attention</h2>

      {error && <p>{error}</p>}

      {!error && applications.length === 0 && (
        <p>No application follow-ups are currently due.</p>
      )}

      {applications.map((application) => (
        <section key={application.application_id}>
          <h3>{application.job_title ?? `Job ${application.job_id}`}</h3>

          {application.company && <p>{application.company}</p>}

          <p>Status: {application.status}</p>

          {application.next_action && (
            <p>Next action: {application.next_action}</p>
          )}

          {application.follow_up_at && (
            <p>Follow up: {application.follow_up_at}</p>
          )}
        </section>
      ))}

      <h2>Recent Activity</h2>

      {!error && activity.length === 0 && <p>No application activity today.</p>}

      {activity.map((event) => (
        <section key={event.event_id}>
          <h3>{event.event_type}</h3>

          <p>
            {event.job_title ??
              (event.job_id
                ? `Job ${event.job_id}`
                : `Application ${event.application_id}`)}
          </p>

          {event.company && <p>{event.company}</p>}

          {event.notes && <p>{event.notes}</p>}

          <p>{event.occurred_at}</p>
        </section>
      ))}

      <h2>Record Activity</h2>

      <form onSubmit={submitActivity}>
        <div>
          <label>
            Application
            <select
              value={activityForm.application_id}
              onChange={(event) =>
                setActivityForm({
                  ...activityForm,
                  application_id: event.target.value,
                })
              }
              required
            >
              <option value="">Select an application</option>

              {trackedApplications.map((application) => (
                <option
                  key={application.application_id}
                  value={application.application_id}
                >
                  {application.job_title ?? `Job ${application.job_id}`}
                  {application.company ? ` — ${application.company}` : ""}
                  {` (${application.status})`}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            Event Type
            <select
              value={activityForm.event_type}
              onChange={(event) =>
                setActivityForm({
                  ...activityForm,
                  event_type: event.target.value,
                })
              }
              required
            >
              <option value="">Select an activity type</option>

              {activityTypes.map((activityType) => (
                <option key={activityType} value={activityType}>
                  {activityType}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            Notes
            <textarea
              value={activityForm.notes}
              onChange={(event) =>
                setActivityForm({
                  ...activityForm,
                  notes: event.target.value,
                })
              }
            />
          </label>
        </div>

        <button type="submit">Record Activity</button>
      </form>

      {submitMessage && <p>{submitMessage}</p>}
    </main>
  );
}

export default App;
