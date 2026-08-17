export type ActivityEvent = {
  event_id: number;
  application_id: number;
  event_type: string;
  occurred_at: string;
  notes: string | null;
  job_id: number | null;
  job_title: string | null;
  company: string | null;
};

type RecentActivityProps = {
  activity: ActivityEvent[];
  error: string | null;
};

export function RecentActivity({ activity, error }: RecentActivityProps) {
  return (
    <>
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
    </>
  );
}
