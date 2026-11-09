import AccountStartScreen from "./AccountStartScreen";

export default function AccountStartPreview() {
  return <div className="app-settings-preview">
    <AccountStartScreen
      previewMode
      onProviderStart={async () => undefined}
      onEmailOtpStart={async () => undefined}
    />
  </div>;
}
