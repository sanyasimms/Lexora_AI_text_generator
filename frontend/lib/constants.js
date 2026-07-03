export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export const LANGUAGE_OPTIONS = [
  { label: 'English', value: 'en' },
  { label: 'Spanish', value: 'es' },
  { label: 'French', value: 'fr' },
  { label: 'German', value: 'de' },
  { label: 'Portuguese', value: 'pt' },
  { label: 'Japanese', value: 'ja' },
  { label: 'Korean', value: 'ko' },
];

export const DEFAULT_STYLES = {
  font_family: 'Space Grotesk, sans-serif',
  font_size: 42,
  text_color: '#F5F7FF',
  background_color: '#08111f',
  bg_opacity: 0.58,
};

export const DEFAULT_SUBTITLES = [
  {
    id: 'cue-1',
    start_time: 0,
    end_time: 2.6,
    text: 'Drop a clip, then tune the subtitles here.',
  },
  {
    id: 'cue-2',
    start_time: 2.8,
    end_time: 5.3,
    text: 'The preview updates as the video plays.',
  },
];