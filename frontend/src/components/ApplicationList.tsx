export type TrackedApplication = {
  application_id: number;
  job_id: number;
  status: string;
  job_title: string | null;
  company: string | null;
};

type ApplicationListProps = {
  applications: TrackedApplication[];
  onSelectApplication: (applicationId: number) => void;
};

export function ApplicationList({
  applications,
  onSelectApplication,
}: ApplicationListProps) {
  return (
    <>
      <h2>Applications</h2>

      {applications.length === 0 && <p>No tracked applications yet.</p>}

      {applications.map((application) => (
        <section key={application.application_id}>
          <button
            type="button"
            onClick={() => onSelectApplication(application.application_id)}
          >
            <h3>{application.job_title ?? `Job ${application.job_id}`}</h3>
          </button>

          {application.company && <p>{application.company}</p>}

          <p>Status: {application.status}</p>
        </section>
      ))}
    </>
  );
}
