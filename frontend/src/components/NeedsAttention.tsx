export type ApplicationAttention = {
  application_id: number;
  job_id: number;
  status: string;
  next_action: string | null;
  follow_up_at: string | null;
  job_title: string | null;
  company: string | null;
};

type NeedsAttentionProps = {
  applications: ApplicationAttention[];
  error: string | null;
};

export function NeedsAttention({ applications, error }: NeedsAttentionProps) {
  return (
    <>
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
    </>
  );
}
