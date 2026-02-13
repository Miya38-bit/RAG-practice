type HeaderProps = {
  onToggleSidebar: () => void;
};

export default function Header({ onToggleSidebar }: HeaderProps) {
  return (
    <header className="sticky top-0 z-10 bg-stone-900/95 backdrop-blur-md border-b border-orange-800/30 shadow-lg">
      <div className="flex items-center gap-4 px-4 py-4 max-w-5xl mx-auto">
        {/* ハンバーガーメニューボタン */}
        <button
          type="button"
          onClick={onToggleSidebar}
          className="p-2 hover:bg-stone-800 rounded-lg transition-colors lg:hidden"
          aria-label="メニューを開く"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>

        {/* タイトル */}
        <h1 className="text-xl font-bold text-orange-100">
          Internal Rules Chatbot
        </h1>
      </div>
    </header>
  );
}
