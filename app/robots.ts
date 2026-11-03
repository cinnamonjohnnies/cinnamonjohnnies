import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/env";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: "*", allow: "/", disallow: ["/app", "/account", "/auth/", "/api/", "/login", "/signup"] }],
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
