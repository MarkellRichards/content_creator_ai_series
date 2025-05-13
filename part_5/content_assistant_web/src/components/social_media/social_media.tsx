import ReactMarkdown from 'react-markdown';
import { SocialMediaType } from '../../services/social_media_posts';
import { Link } from '@tanstack/react-router';

type SocialMediaProps = {
  social_media: SocialMediaType;
};

const SocialMediaCard: React.FC<SocialMediaProps> = ({ social_media }) => {
  return (
    <Link
      to="/social_media/$social_mediaId"
      params={{ social_mediaId: social_media.guid }}
    >
      <div className="max-w-sm rounded overflow-hidden shadow-lg p-4 bg-white h-full">
        <img
          className="w-full h-48 object-fill"
          src={social_media.image_url}
          alt={'image related to content'}
        />
        <div className="px-6 py-4">
          <div className="text-gray-700 text-base line-clamp-5">
            <ReactMarkdown>{social_media.content}</ReactMarkdown>
          </div>
        </div>
        <div className="px-6 pt-4 pb-2">
          <p className="text-gray-600 text-sm">
            {new Date(social_media.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </Link>
  );
};

export default SocialMediaCard;
