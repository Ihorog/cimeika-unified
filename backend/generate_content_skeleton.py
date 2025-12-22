#!/usr/bin/env python3
"""
Content Skeleton Generator for SEO Matrix
Generates 49 page skeletons for Cimeika Family Memory & Planning Hub
"""
import sys
import os
from pathlib import Path
import yaml

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.config.seo.seo_matrix_service import get_seo_matrix_service


# Page templates
PAGE_TEMPLATE_EN = """---
title: "{title}"
description: "{description}"
module: {module}
category: {category}
intent: {intent}
lang: en
canonical: /en/{slug}
alternates:
  uk: /ua/{slug}
---

# {title}

{description}

## Overview

[Content to be added]

## Key Features

- Feature 1
- Feature 2
- Feature 3

## How to Use

1. Step 1
2. Step 2
3. Step 3

## Related Pages

{related_links}

## Get Started

{cta}
"""

PAGE_TEMPLATE_UA = """---
title: "{title}"
description: "{description}"
module: {module}
category: {category}
intent: {intent}
lang: uk
canonical: /ua/{slug}
alternates:
  en: /en/{slug}
---

# {title}

{description}

## Огляд

[Контент буде додано]

## Ключові можливості

- Можливість 1
- Можливість 2
- Можливість 3

## Як використовувати

1. Крок 1
2. Крок 2
3. Крок 3

## Пов'язані сторінки

{related_links}

## Розпочати

{cta}
"""


def generate_title_en(module_name, category_name, intent):
    """Generate English title"""
    category_titles = {
        'use_cases': f'{module_name} Use Cases',
        'how_to': f'How to Use {module_name}',
        'templates': f'{module_name} Templates',
        'examples': f'{module_name} Examples',
        'features': f'{module_name} Features',
        'problems': f'{module_name} Troubleshooting',
        'comparisons': f'{module_name} Comparisons'
    }
    return category_titles.get(category_name, f'{module_name} - {category_name}')


def generate_title_ua(module_name, category_name, intent):
    """Generate Ukrainian title"""
    category_titles = {
        'use_cases': f'Сценарії використання {module_name}',
        'how_to': f'Як використовувати {module_name}',
        'templates': f'Шаблони {module_name}',
        'examples': f'Приклади {module_name}',
        'features': f'Можливості {module_name}',
        'problems': f'Вирішення проблем {module_name}',
        'comparisons': f'Порівняння {module_name}'
    }
    return category_titles.get(category_name, f'{module_name} - {category_name}')


def generate_description_en(module_name, category_name, intent):
    """Generate English description"""
    return f"Learn how to use {module_name} for {intent}. Complete guide with examples and best practices."


def generate_description_ua(module_name, category_name, intent):
    """Generate Ukrainian description"""
    return f"Дізнайтеся, як використовувати {module_name} для {intent}. Повний посібник з прикладами та рекомендаціями."


def generate_page_content(page, lang='en', service=None):
    """Generate page content from page data"""
    module = page['module']
    category = page['category']
    intent = page['intent']
    slug = page['slug']
    
    # Get module info
    module_info = service.get_module(module) if service else None
    module_name = module_info['name'] if module_info else module.title()
    
    # Generate content
    if lang == 'en':
        title = generate_title_en(module_name, category, intent)
        description = generate_description_en(module_name, category, intent)
        template = PAGE_TEMPLATE_EN
        cta = service.primary_cta if service else "Get Started"
    else:
        title = generate_title_ua(module_name, category, intent)
        description = generate_description_ua(module_name, category, intent)
        template = PAGE_TEMPLATE_UA
        cta = service.primary_cta if service else "Розпочати"
    
    # Generate related links (placeholder)
    related_links = "- [Link 1](#)\n- [Link 2](#)\n- [Link 3](#)"
    
    content = template.format(
        title=title,
        description=description,
        module=module,
        category=category,
        intent=intent,
        slug=slug,
        related_links=related_links,
        cta=cta
    )
    
    return content


def generate_all_pages(output_dir='content', dry_run=False):
    """Generate all page skeletons"""
    print("=" * 60)
    print("CONTENT SKELETON GENERATOR")
    print("Family Memory & Planning Hub")
    print("=" * 60)
    
    # Initialize service
    service = get_seo_matrix_service()
    
    # Get all pages
    pages = service.get_all_pages()
    print(f"\nGenerating {len(pages)} page skeletons...")
    print(f"Output directory: {output_dir}")
    print(f"Dry run: {dry_run}")
    
    if not dry_run:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    generated_count = 0
    skipped_count = 0
    
    for page in pages:
        slug = page['slug']
        module = page['module']
        
        # Generate both languages
        for lang in ['en', 'ua']:
            # Create file path
            if lang == 'en':
                file_path = Path(output_dir) / 'en' / f"{slug}.md"
            else:
                file_path = Path(output_dir) / 'ua' / f"{slug}.md"
            
            # Check if file exists
            if not dry_run and file_path.exists():
                print(f"  ⊙ Skip (exists): {file_path}")
                skipped_count += 1
                continue
            
            # Generate content
            content = generate_page_content(page, lang, service)
            
            if dry_run:
                print(f"  ✓ Would create: {file_path}")
            else:
                # Create directory
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✓ Created: {file_path}")
            
            generated_count += 1
    
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total pages: {len(pages)}")
    print(f"Generated: {generated_count} files")
    print(f"Skipped: {skipped_count} files")
    print(f"Languages: en, ua")
    
    if dry_run:
        print("\nNote: This was a dry run. No files were created.")
        print("Run without --dry-run to actually generate files.")
    else:
        print(f"\n✓ Files saved to: {output_dir}/")
    
    return generated_count


def generate_index_page(output_dir='content', lang='en'):
    """Generate index page with all modules and categories"""
    service = get_seo_matrix_service()
    
    if lang == 'en':
        title = "Cimeika - Family Memory & Planning Hub"
        description = service.core_promise
        content = f"""---
title: "{title}"
description: "{description}"
lang: en
---

# {title}

{description}

## Modules

"""
    else:
        title = "Cimeika - Родинний простір для спогадів та планування"
        description = service.core_promise
        content = f"""---
title: "{title}"
description: "{description}"
lang: uk
---

# {title}

{description}

## Модулі

"""
    
    # Add modules
    modules = service.get_modules()
    for module in modules:
        content += f"\n### {module['name']}\n"
        content += f"{module['role']}\n\n"
        
        # Add categories for this module
        patterns = service.get_all_patterns(module['id'])
        if module['id'] in patterns:
            content += "**Content:**\n"
            for category_id, pattern in patterns[module['id']].items():
                if pattern and 'pages' in pattern:
                    for page_slug in pattern['pages']:
                        page_name = page_slug.split('/')[-1].replace('-', ' ').title()
                        content += f"- [{page_name}](/{lang}/{page_slug})\n"
        content += "\n"
    
    # Add CTA
    if lang == 'en':
        content += f"\n## {service.primary_cta}\n\n"
        content += "[Get Started →](/en/ci/how-to-start)\n"
    else:
        content += f"\n## {service.primary_cta}\n\n"
        content += "[Розпочати →](/ua/ci/how-to-start)\n"
    
    # Write file
    file_path = Path(output_dir) / lang / 'index.md'
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created index: {file_path}")
    return file_path


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate content skeletons for SEO matrix')
    parser.add_argument('--output', '-o', default='content', help='Output directory (default: content)')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Dry run - show what would be created')
    parser.add_argument('--index', '-i', action='store_true', help='Also generate index pages')
    
    args = parser.parse_args()
    
    try:
        # Generate pages
        count = generate_all_pages(args.output, args.dry_run)
        
        # Generate index pages if requested
        if args.index and not args.dry_run:
            print("\nGenerating index pages...")
            generate_index_page(args.output, 'en')
            generate_index_page(args.output, 'ua')
        
        print("\n✓ Content generation complete!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
