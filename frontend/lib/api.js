import { API_BASE_URL } from './constants';

function getErrorMessage(responseBody, fallbackMessage) {
  if (!responseBody) {
    return fallbackMessage;
  }

  if (typeof responseBody === 'string') {
    return responseBody;
  }

  if (typeof responseBody.detail === 'string') {
    return responseBody.detail;
  }

  return fallbackMessage;
}

export function updateSubtitleId(subtitle, index = 0) {
  return {
    ...subtitle,
    id: subtitle.id || `cue-${index + 1}-${Math.random().toString(36).slice(2, 7)}`,
  };
}

export function buildActiveSubtitleId(subtitles, currentTime) {
  const activeSubtitle = subtitles.find(
    (subtitle) => currentTime >= subtitle.start_time && currentTime <= subtitle.end_time,
  );

  return activeSubtitle?.id ?? subtitles[0]?.id ?? '';
}

export async function transcribeAndTranslate(videoFile, targetLanguage) {
  const formData = new FormData();
  formData.append('video_file', videoFile);
  formData.append('target_language', targetLanguage);

  const response = await fetch(`${API_BASE_URL}/transcribe-translate`, {
    method: 'POST',
    body: formData,
  });

  const responseBody = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(getErrorMessage(responseBody, 'Failed to transcribe and translate the selected video.'));
  }

  return {
    ...responseBody,
    subtitles: responseBody.subtitles.map(updateSubtitleId),
  };
}

export async function exportVideo(videoFile, subtitles, styles) {
  const formData = new FormData();
  formData.append('video_file', videoFile);
  formData.append('subtitles', JSON.stringify(subtitles));
  formData.append('styles', JSON.stringify(styles));

  const response = await fetch(`${API_BASE_URL}/export-video`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const responseBody = await response.json().catch(() => null);
    throw new Error(getErrorMessage(responseBody, 'Failed to export the captioned video.'));
  }

  const blob = await response.blob();
  const disposition = response.headers.get('content-disposition') || '';
  const fileMatch = disposition.match(/filename="?([^";]+)"?/i);

  return {
    blob,
    filename: fileMatch?.[1] || 'captioned-video.mp4',
  };
}