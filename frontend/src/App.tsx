import { useEffect, useState } from "react";

import {
  NeedsAttention,
  type ApplicationAttention,
} from "./components/NeedsAttention";

import {
  RecentActivity,
  type ActivityEvent,
} from "./components/RecentActivity";

import {
  RecordActivity,
  type ActivityForm,
  type TrackedApplication,
} from "./components/RecordActivity";

import { ApplicationList } from "./components/ApplicationList";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [applications, setApplications] = useState<ApplicationAttention[]>([]);

  const [trackedApplications, setTrackedApplications] = useState<
    TrackedApplication[]
  >([]);

  const [selectedApplicationId, setSelectedApplicationId] = useState<
    number | null
  >(null);

  const [selectedApplicationActivity, setSelectedApplicationActivity] =
    useState<ActivityEvent[]>([]);

  const [statusNote, setStatusNote] = useState("");

  const selectedApplication =
    trackedApplications.find(
      (application) => application.application_id === selectedApplicationId,
    ) ?? null;

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
    fetch(`${API_BASE_URL}/activity/today`)
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

  function loadTrackedApplications() {
    fetch(`${API_BASE_URL}/applications`)
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
  }

  function loadSelectedApplicationActivity(applicationId: number) {
    fetch(`${API_BASE_URL}/applications/${applicationId}/activity`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load application history");
        }

        return response.json();
      })
      .then((data) => {
        setSelectedApplicationActivity(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }

  function submitActivity(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    fetch(`${API_BASE_URL}/activity`, {
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

  function markClosed() {
    if (selectedApplicationId === null) {
      return;
    }

    fetch(`${API_BASE_URL}/applications/${selectedApplicationId}/mark-closed`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        notes: statusNote || null,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to close application");
        }

        return response.json();
      })
      .then(() => {
        setStatusNote("");
        loadTrackedApplications();
        loadSelectedApplicationActivity(selectedApplicationId);
      })
      .catch((err) => {
        setError(err.message);
      });
  }

  function markWithdrawn() {
    if (selectedApplicationId === null) {
      return;
    }

    fetch(
      `${API_BASE_URL}/applications/${selectedApplicationId}/mark-withdrawn`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: statusNote || null,
        }),
      },
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to mark application withdrawn");
        }

        return response.json();
      })
      .then(() => {
        setStatusNote("");
        loadTrackedApplications();
        loadSelectedApplicationActivity(selectedApplicationId);
      })
      .catch((err) => {
        setError(err.message);
      });
  }

  function markRejected() {
    if (selectedApplicationId === null) {
      return;
    }

    fetch(
      `${API_BASE_URL}/applications/${selectedApplicationId}/mark-rejected`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: statusNote || null,
        }),
      },
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to mark application rejected");
        }

        return response.json();
      })
      .then(() => {
        setStatusNote("");
        loadTrackedApplications();
        loadSelectedApplicationActivity(selectedApplicationId);
      })
      .catch((err) => {
        setError(err.message);
      });
  }

  useEffect(() => {
    fetch(`${API_BASE_URL}/applications/needs-attention`)
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

    loadTrackedApplications();

    fetch(`${API_BASE_URL}/activity-types`)
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

  useEffect(() => {
    if (selectedApplicationId === null) {
      setSelectedApplicationActivity([]);
      return;
    }

    loadSelectedApplicationActivity(selectedApplicationId);
  }, [selectedApplicationId]);

  return (
    <main>
      <h1>AI Career Manager</h1>

      <NeedsAttention applications={applications} error={error} />

      <ApplicationList
        applications={trackedApplications}
        onSelectApplication={setSelectedApplicationId}
      />

      {selectedApplication && (
        <section>
          <h2>Application Details</h2>

          <h3>
            {selectedApplication.job_title ??
              `Job ${selectedApplication.job_id}`}
          </h3>

          {selectedApplication.company && <p>{selectedApplication.company}</p>}

          <p>Status: {selectedApplication.status}</p>

          <h3>Activity History</h3>

          <div>
            <label>
              Status note
              <textarea
                value={statusNote}
                onChange={(event) => setStatusNote(event.target.value)}
              />
            </label>
          </div>

          <button type="button" onClick={markClosed}>
            Mark Closed
          </button>

          <button type="button" onClick={markWithdrawn}>
            Mark Withdrawn
          </button>

          <button type="button" onClick={markRejected}>
            Mark Rejected
          </button>

          {selectedApplicationActivity.length === 0 && (
            <p>No activity recorded for this application.</p>
          )}

          {selectedApplicationActivity.map((event) => (
            <section key={event.event_id}>
              <p>{event.event_type}</p>

              {event.notes && <p>{event.notes}</p>}

              <p>{event.occurred_at}</p>
            </section>
          ))}
        </section>
      )}

      <RecentActivity activity={activity} error={error} />

      <RecordActivity
        trackedApplications={trackedApplications}
        activityTypes={activityTypes}
        activityForm={activityForm}
        submitMessage={submitMessage}
        onFormChange={setActivityForm}
        onSubmit={submitActivity}
      />
    </main>
  );
}

export default App;
