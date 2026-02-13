/**
 * コンテナーコンポーネント
 * @param children 子要素
 * @param className クラス名
 */
export default function Container({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`max-w-7xl mx-auto ${className}`}>{children}</div>;
}
