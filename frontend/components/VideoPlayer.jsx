import { forwardRef } from 'react';

function hexToRgba(hexColor, alpha) {
  const normalizedHex = hexColor.replace('#', '').trim();
  const fullHex = normalizedHex.length === 3
    ? normalizedHex.split('').map((character) => character + character).join('')
    : normalizedHex;

  if (fullHex.length !== 6) {
    return `rgba(0, 0, 0, ${alpha})`;
  }

  const red = Number.parseInt(fullHex.slice(0, 2), 16);
  const green = Number.parseInt(fullHex.slice(2, 4), 16);
  const blue = Number.parseInt(fullHex.slice(4, 6), 16);

  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}

const VideoPlayer = forwardRef(function VideoPlayer(
  { videoUrl, subtitles, styles, currentSubtitle, onTimeUpdate },
  ref,
) {
  return (
    <section className="panel panel--video">
      <div className="panel__header">
        <div>
          <p className="panel__eyebrow">Preview</p>
          <h2>Live subtitle overlay</h2>
        </div>
        <div className="upload-pill">{subtitles.length} cues</div>
      </div>

      <div className="video-stage">
        {videoUrl ? (
          <video ref={ref} className="video-stage__media" controls src={videoUrl} onTimeUpdate={onTimeUpdate} />
        ) : (
          <div className="video-stage__empty">
            <p>No video loaded yet.</p>
            <span>Preview styling and subtitle timing once a file is selected.</span>
          </div>
        )}

        <div
          className="video-stage__subtitle"
          style={{
            color: styles.text_color,
            fontFamily: styles.font_family,
            fontSize: `${styles.font_size}px`,
            backgroundColor: hexToRgba(styles.background_color, styles.bg_opacity),
          }}
        >
          <span>{currentSubtitle?.text || 'Subtitle preview appears here.'}</span>
        </div>
      </div>
    </section>
  );
});

export default VideoPlayer;