'use client';

const featureCards = [
  {
    title: 'Upload and transcribe',
    description: 'Send a video to the backend, extract subtitles, and keep the workflow simple from the start.',
  },
  {
    title: 'Live style controls',
    description: 'Adjust font, color, background, and opacity while seeing the caption treatment update instantly.',
  },
  {
    title: 'Subtitle editor',
    description: 'Edit subtitle text and timing in a clean timeline view before exporting the final result.',
  },
  {
    title: 'Burn-in export',
    description: 'Render a finished MP4 with styled subtitles using the backend FFmpeg pipeline.',
  },
  {
    title: '3D presentation',
    description: 'Use layered cards, perspective, and tilt effects to make the landing feel more tactile.',
  },
];

export default function FeaturesPage() {
  return (
    <main className="landing-shell landing-shell--features">
      <section className="features-hero card-3d">
        <div className="features-hero__copy">
          <p className="eyebrow">Lexora features</p>
          <h1>Everything you need for a tighter caption workflow.</h1>
          <p>
            The homepage gives the pitch. This page shows the building blocks behind it: upload, style, edit, preview,
            and export.
          </p>
        </div>

        <a className="button button--secondary features-hero__back" href="/">
          Back to landing
        </a>
      </section>

      <section className="feature-grid">
        {featureCards.map((feature, index) => (
          <article key={feature.title} className={`feature-card card-3d card-3d--${index % 3}`}>
            <div className="feature-card__index">0{index + 1}</div>
            <h2>{feature.title}</h2>
            <p>{feature.description}</p>
          </article>
        ))}
      </section>
    </main>
  );
}