import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/env";
import { allArticles } from "@/lib/library";

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ["", "/pricing", "/help", "/library", "/terms", "/privacy"].map((p) => ({ url: `${SITE_URL}${p}`, changeFrequency: "monthly" as const }));
  const arts = allArticles().map((a) => ({ url: `${SITE_URL}/library/${a.slug}`, changeFrequency: "monthly" as const }));
  return [...pages, ...arts];
}
