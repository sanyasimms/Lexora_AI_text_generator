export default function SubtitleEditor({ subtitles, activeSubtitleId, onSubtitleChange, onAddSubtitle, onRemoveSubtitle }) {
  return (
    <section className="panel">
      <div className="panel__header">
        <div>
          <p className="panel__eyebrow">Editor</p>
          <h2>Subtitle timeline</h2>
        </div>
        <button className="button button--ghost" type="button" onClick={onAddSubtitle}>
          Add cue
        </button>
      </div>

      <div className="subtitle-list">
        {subtitles.map((subtitle, index) => (
          <article key={subtitle.id} className={`subtitle-row ${subtitle.id === activeSubtitleId ? 'subtitle-row--active' : ''}`}>
            <div className="subtitle-row__meta">
              <span>#{String(index + 1).padStart(2, '0')}</span>
              <button className="button button--ghost button--ghost-danger" type="button" onClick={() => onRemoveSubtitle(subtitle.id)}>
                Remove
              </button>
            </div>

            <div className="subtitle-row__fields">
              <label className="field">
                <span>Start</span>
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={subtitle.start_time}
                  onChange={(event) => onSubtitleChange(subtitle.id, 'start_time', event.target.value)}
                />
              </label>

              <label className="field">
                <span>End</span>
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={subtitle.end_time}
                  onChange={(event) => onSubtitleChange(subtitle.id, 'end_time', event.target.value)}
                />
              </label>

              <label className="field field--full">
                <span>Text</span>
                <textarea
                  rows="2"
                  value={subtitle.text}
                  onChange={(event) => onSubtitleChange(subtitle.id, 'text', event.target.value)}
                />
              </label>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}