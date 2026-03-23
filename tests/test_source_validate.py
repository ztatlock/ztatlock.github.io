from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.source_validate import find_source_issues


class SourceValidateTests(unittest.TestCase):
    def test_reports_invalid_talk_bundle_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "index.dj").write_text(
                "---\n"
                "description: Home\n"
                "---\n"
                "# Home\n",
                encoding="utf-8",
            )
            (pages / "talks.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n"
                "# Talks\n\n"
                "__TALKS_LIST__\n",
                encoding="utf-8",
            )

            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{talk_dir / 'talk.json'}.when: must provide exactly one of month or season"],
            )

    def test_reports_missing_talks_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "talks.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n"
                "# Talks\n\n"
                "Manual list.\n",
                encoding="utf-8",
            )

            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'talks.dj'}: talks page must contain __TALKS_LIST__"],
            )

    def test_accepts_configured_static_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/demo.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )
            (img_dir / "demo.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_configured_static_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/missing.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'about.dj'}: image path does not exist: img/missing.png"],
            )

    def test_reports_missing_front_matter_for_pub_prefix_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            page_path = pages / "pub-demo.dj"
            page_path.write_text("# Demo\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{page_path}: missing front matter metadata"],
            )

    def test_accepts_publication_local_metadata_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "meta_image_path": "pubs/2025-test-demo/custom-meta.png",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (pub_dir / "custom-meta.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_publication_metadata_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "meta_image_path": "pubs/2025-test-demo/missing-meta.png",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pub_dir / 'publication.json'}: image path does not exist: pubs/2025-test-demo/missing-meta.png"
                ],
            )

    def test_reports_legacy_publication_link_in_page_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            page_path = pages / "index.dj"
            page_path.write_text(
                "---\n"
                "description: Demo description\n"
                "---\n"
                "# Home\n\nSee [paper](pub-2024-asplos-lakeroad.html).\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{page_path}: legacy publication link should use canonical publication path: "
                    "pub-2024-asplos-lakeroad.html -> pubs/2024-asplos-lakeroad/"
                ],
            )

    def test_reports_legacy_publication_link_in_publication_extra_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            extra_path = pubs / "2025-test-demo" / "extra.dj"
            extra_path.parent.mkdir()
            extra_path.write_text(
                "See [older paper](pub-2024-asplos-lakeroad.html).\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{extra_path}: legacy publication link should use canonical publication path: "
                    "pub-2024-asplos-lakeroad.html -> pubs/2024-asplos-lakeroad/"
                ],
            )

    def test_reports_root_layout_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            (root / "about.dj").write_text("# About\n", encoding="utf-8")
            (root / "robots.txt").write_text("User-agent: *\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset/>\n", encoding="utf-8")
            (root / "img").mkdir()
            (root / "templates").mkdir()
            (root / "pubs").mkdir()

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{root / 'about.dj'}: authored Djot source must live under site/pages/",
                    f"{root / 'sitemap.xml'}: generated sitemap belongs only under build/",
                    f"{root / 'robots.txt'}: static assets must live under site/static/",
                    f"{root / 'img'}: shared images must live under site/static/img/",
                    f"{root / 'pubs'}: publication bundles must live under site/pubs/",
                    f"{root / 'templates'}: templates must live under site/templates/",
                ],
            )
