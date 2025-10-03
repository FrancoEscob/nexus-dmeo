import {HeroSection} from "@/components/landing/HeroSection";
import {DemoFlowPreview} from "@/components/landing/DemoFlowPreview";
import {DemoExperienceSection} from "@/components/demo/DemoExperienceSection";
import {LanguagesHighlight} from "@/components/landing/LanguagesHighlight";
import {UpcomingFeaturesSection} from "@/components/landing/UpcomingFeaturesSection";

export default function LandingPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-16 px-6 py-24">
      <HeroSection />
      <DemoFlowPreview />
      <DemoExperienceSection />
      <LanguagesHighlight />
      <UpcomingFeaturesSection />
    </main>
  );
}
