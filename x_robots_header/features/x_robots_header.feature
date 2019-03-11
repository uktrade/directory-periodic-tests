Feature: Every page on non-production site should return "X-Robots-Tag: noindex" header


    @TT-281
    @CMS-306
    @<environment>
    @<service>
    Scenario Outline: Response from (<environment>) "<service>" "<page>" should contain "X-Robots-Tag: noindex" header
        When you visit "<page>" on "<service>" (<environment>) 

        Then the response should contain "X-Robots-Tag: noindex" header

        Examples: <environment> <service>
            | environment | service | page                                                                                             |
            | DEV         | Invest  | /                                                                                                |
            | DEV         | Invest  | /contact/                                                                                        |
            | DEV         | Invest  | /feedback/                                                                                       |
            | DEV         | Invest  | /industries/                                                                                     |
            | DEV         | Invest  | /industries/advanced-manufacturing/                                                              |
            | DEV         | Invest  | /industries/aerospace/                                                                           |
            | DEV         | Invest  | /industries/agri-tech/                                                                           |
            | DEV         | Invest  | /industries/automotive/                                                                          |
            | DEV         | Invest  | /industries/automotive/automotive-research-and-development/                                      |
            | DEV         | Invest  | /industries/automotive/automotive-supply-chain/                                                  |
            | DEV         | Invest  | /industries/automotive/motorsport/                                                               |
            | DEV         | Invest  | /industries/capital-investment/                                                                  |
            | DEV         | Invest  | /industries/chemicals/                                                                           |
            | DEV         | Invest  | /industries/creative-industries/                                                                 |
            | DEV         | Invest  | /industries/creative-industries/creative-content-and-production/                                 |
            | DEV         | Invest  | /industries/creative-industries/digital-media/                                                   |
            | DEV         | Invest  | /industries/energy/                                                                              |
            | DEV         | Invest  | /industries/energy/electrical-networks/                                                          |
            | DEV         | Invest  | /industries/energy/energy-waste/                                                                 |
            | DEV         | Invest  | /industries/energy/nuclear-energy/                                                               |
            | DEV         | Invest  | /industries/energy/offshore-wind-energy/                                                         |
            | DEV         | Invest  | /industries/energy/oil-and-gas/                                                                  |
            | DEV         | Invest  | /industries/financial-services/                                                                  |
            | DEV         | Invest  | /industries/financial-services/asset-management/                                                 |
            | DEV         | Invest  | /industries/financial-services/financial-technology/                                             |
            | DEV         | Invest  | /industries/food-and-drink/                                                                      |
            | DEV         | Invest  | /industries/food-and-drink/food-service-and-catering/                                            |
            | DEV         | Invest  | /industries/food-and-drink/free-foods/                                                           |
            | DEV         | Invest  | /industries/food-and-drink/meat-poultry-and-dairy/                                               |
            | DEV         | Invest  | /industries/health-and-life-sciences/                                                            |
            | DEV         | Invest  | /industries/health-and-life-sciences/medical-technology/                                         |
            | DEV         | Invest  | /industries/health-and-life-sciences/pharmaceutical-manufacturing/                               |
            | DEV         | Invest  | /industries/retail/                                                                              |
            | DEV         | Invest  | /industries/technology/                                                                          |
            | DEV         | Invest  | /industries/technology/data-analytics/                                                           |
            | DEV         | Invest  | /privacy-and-cookies/                                                                            |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-export-opportunities/                                |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-export-readiness/                                    |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-for-smart-survey/                                    |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-invest-in-great-britain/                             |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-selling-online-overseas/                             |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-trade-profiles-find-a-buyer-fab-find-a-supplier-fas/ |
            | DEV         | Invest  | /privacy-and-cookies/fair-processing-notice-zendesk/                                             |
            | DEV         | Invest  | /terms-and-conditions/                                                                           |
            | DEV         | Invest  | /uk-regions/london/                                                                              |
            | DEV         | Invest  | /uk-regions/midlands/                                                                            |
            | DEV         | Invest  | /uk-regions/north-england/                                                                       |
            | DEV         | Invest  | /uk-regions/northern-ireland/                                                                    |
            | DEV         | Invest  | /uk-regions/scotland/                                                                            |
            | DEV         | Invest  | /uk-regions/south-england/                                                                       |
            | DEV         | Invest  | /uk-regions/wales/                                                                               |
            | DEV         | Invest  | /uk-setup-guide/                                                                                 |
            | DEV         | Invest  | /uk-setup-guide/apply-uk-visa/                                                                   |
            | DEV         | Invest  | /uk-setup-guide/establish-base-business-uk/                                                      |
            | DEV         | Invest  | /uk-setup-guide/hire-skilled-workers-your-uk-operations/                                         |
            | DEV         | Invest  | /uk-setup-guide/open-uk-business-bank-account/                                                   |
            | DEV         | Invest  | /uk-setup-guide/setup-your-business-uk/                                                          |
            | DEV         | Invest  | /uk-setup-guide/understand-uk-tax-and-incentives/                                                |


        @wip
        @NO_STAGING_ENV
        Examples: <environment> <service>
            | environment | service | page                                                                                             |
            | STAGE       | Invest  | /                                                                                                |
            | STAGE       | Invest  | /contact/                                                                                        |
            | STAGE       | Invest  | /feedback/                                                                                       |
            | STAGE       | Invest  | /industries/                                                                                     |
            | STAGE       | Invest  | /industries/advanced-manufacturing/                                                              |
            | STAGE       | Invest  | /industries/aerospace/                                                                           |
            | STAGE       | Invest  | /industries/agri-tech/                                                                           |
            | STAGE       | Invest  | /industries/automotive/                                                                          |
            | STAGE       | Invest  | /industries/automotive/automotive-research-and-development/                                      |
            | STAGE       | Invest  | /industries/automotive/automotive-supply-chain/                                                  |
            | STAGE       | Invest  | /industries/automotive/motorsport/                                                               |
            | STAGE       | Invest  | /industries/capital-investment/                                                                  |
            | STAGE       | Invest  | /industries/chemicals/                                                                           |
            | STAGE       | Invest  | /industries/creative-industries/                                                                 |
            | STAGE       | Invest  | /industries/creative-industries/creative-content-and-production/                                 |
            | STAGE       | Invest  | /industries/creative-industries/digital-media/                                                   |
            | STAGE       | Invest  | /industries/energy/                                                                              |
            | STAGE       | Invest  | /industries/energy/electrical-networks/                                                          |
            | STAGE       | Invest  | /industries/energy/energy-waste/                                                                 |
            | STAGE       | Invest  | /industries/energy/nuclear-energy/                                                               |
            | STAGE       | Invest  | /industries/energy/offshore-wind-energy/                                                         |
            | STAGE       | Invest  | /industries/energy/oil-and-gas/                                                                  |
            | STAGE       | Invest  | /industries/financial-services/                                                                  |
            | STAGE       | Invest  | /industries/financial-services/asset-management/                                                 |
            | STAGE       | Invest  | /industries/financial-services/financial-technology/                                             |
            | STAGE       | Invest  | /industries/food-and-drink/                                                                      |
            | STAGE       | Invest  | /industries/food-and-drink/food-service-and-catering/                                            |
            | STAGE       | Invest  | /industries/food-and-drink/free-foods/                                                           |
            | STAGE       | Invest  | /industries/food-and-drink/meat-poultry-and-dairy/                                               |
            | STAGE       | Invest  | /industries/health-and-life-sciences/                                                            |
            | STAGE       | Invest  | /industries/health-and-life-sciences/medical-technology/                                         |
            | STAGE       | Invest  | /industries/health-and-life-sciences/pharmaceutical-manufacturing/                               |
            | STAGE       | Invest  | /industries/retail/                                                                              |
            | STAGE       | Invest  | /industries/technology/                                                                          |
            | STAGE       | Invest  | /industries/technology/data-analytics/                                                           |
            | STAGE       | Invest  | /privacy-and-cookies/                                                                            |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-export-opportunities/                                |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-export-readiness/                                    |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-for-smart-survey/                                    |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-invest-in-great-britain/                             |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-selling-online-overseas/                             |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-trade-profiles-find-a-buyer-fab-find-a-supplier-fas/ |
            | STAGE       | Invest  | /privacy-and-cookies/fair-processing-notice-zendesk/                                             |
            | STAGE       | Invest  | /terms-and-conditions/                                                                           |
            | STAGE       | Invest  | /uk-regions/london/                                                                              |
            | STAGE       | Invest  | /uk-regions/midlands/                                                                            |
            | STAGE       | Invest  | /uk-regions/north-england/                                                                       |
            | STAGE       | Invest  | /uk-regions/northern-ireland/                                                                    |
            | STAGE       | Invest  | /uk-regions/scotland/                                                                            |
            | STAGE       | Invest  | /uk-regions/south-england/                                                                       |
            | STAGE       | Invest  | /uk-regions/wales/                                                                               |
            | STAGE       | Invest  | /uk-setup-guide/                                                                                 |
            | STAGE       | Invest  | /uk-setup-guide/apply-uk-visa/                                                                   |
            | STAGE       | Invest  | /uk-setup-guide/establish-base-business-uk/                                                      |
            | STAGE       | Invest  | /uk-setup-guide/hire-skilled-workers-your-uk-operations/                                         |
            | STAGE       | Invest  | /uk-setup-guide/open-uk-business-bank-account/                                                   |
            | STAGE       | Invest  | /uk-setup-guide/setup-your-business-uk/                                                          |
            | STAGE       | Invest  | /uk-setup-guide/understand-uk-tax-and-incentives/                                                |


        Examples: <environment> <service>
            | environment | service | page                                                                  |
            | DEV         | FAS     | /                                                                     |
            | DEV         | FAS     | case-study/1000/an-international-profession/                          |
            | DEV         | FAS     | case-study/1004/england-and-wales-a-global-legal-centre/              |
            | DEV         | FAS     | case-study/1010/port-comprehensive-assessment-operations-and-manag/   |
            | DEV         | FAS     | case-study/102/livingskin-for-passive-prostheses/                     |
            | DEV         | FAS     | case-study/1022/spl-launches-brochure-for-the-homebrew-industry/      |
            | DEV         | FAS     | case-study/23/bp/                                                     |
            | DEV         | FAS     | case-study/230/poland-sees-its-first-bio-diesel-generators/           |
            | DEV         | FAS     | feedback/                                                             |
            | DEV         | FAS     | industries/                                                           |
            | DEV         | FAS     | industries/aerospace/                                                 |
            | DEV         | FAS     | industries/agritech/                                                  |
            | DEV         | FAS     | industries/automotive/                                                |
            | DEV         | FAS     | industries/business-and-government-partnerships/                      |
            | DEV         | FAS     | industries/business-and-government-partnerships/needs                 |
            | DEV         | FAS     | industries/consumer-retail/                                           |
            | DEV         | FAS     | industries/contact/                                                   |
            | DEV         | FAS     | industries/contact/aerospace/                                         |
            | DEV         | FAS     | industries/contact/agritech/                                          |
            | DEV         | FAS     | industries/contact/automotive/                                        |
            | DEV         | FAS     | industries/contact/business-and-government-partnerships/              |
            | DEV         | FAS     | industries/contact/consumer-retail/                                   |
            | DEV         | FAS     | industries/contact/creative-services/                                 |
            | DEV         | FAS     | industries/contact/cyber-security/                                    |
            | DEV         | FAS     | industries/contact/education-industry/                                |
            | DEV         | FAS     | industries/contact/energy/                                            |
            | DEV         | FAS     | industries/contact/engineering-industry/                              |
            | DEV         | FAS     | industries/contact/food-and-drink/                                    |
            | DEV         | FAS     | industries/contact/healthcare/                                        |
            | DEV         | FAS     | industries/contact/infrastructure/                                    |
            | DEV         | FAS     | industries/contact/innovation-industry/                               |
            | DEV         | FAS     | industries/contact/legal-services/                                    |
            | DEV         | FAS     | industries/contact/life-sciences/                                     |
            | DEV         | FAS     | industries/contact/marine/                                            |
            | DEV         | FAS     | industries/contact/professional-and-financial-services/               |
            | DEV         | FAS     | industries/contact/space/                                             |
            | DEV         | FAS     | industries/contact/sports-economy/                                    |
            | DEV         | FAS     | industries/contact/technology/                                        |
            | DEV         | FAS     | industries/creative-services/                                         |
            | DEV         | FAS     | industries/cyber-security/                                            |
            | DEV         | FAS     | industries/education-industry/                                        |
            | DEV         | FAS     | industries/energy/                                                    |
            | DEV         | FAS     | industries/engineering-industry/                                      |
            | DEV         | FAS     | industries/food-and-drink/                                            |
            | DEV         | FAS     | industries/healthcare/                                                |
            | DEV         | FAS     | industries/infrastructure/                                            |
            | DEV         | FAS     | industries/innovation-industry/                                       |
            | DEV         | FAS     | industries/legal-services/                                            |
            | DEV         | FAS     | industries/life-sciences/                                             |
            | DEV         | FAS     | industries/marine/                                                    |
            | DEV         | FAS     | industries/professional-and-financial-services/                       |
            | DEV         | FAS     | industries/space/                                                     |
            | DEV         | FAS     | industries/sports-economy/                                            |
            | DEV         | FAS     | industries/technology/                                                |
            | DEV         | FAS     | industry-articles/UK-agritech-strengths-article/                      |
            | DEV         | FAS     | industry-articles/a-focus-on-regulatory-technology-solutions-article/ |
            | DEV         | FAS     | industry-articles/a-global-centre-for-life-sciences/                  |
            | DEV         | FAS     | industry-articles/building-fintech-bridges-article/                   |
            | DEV         | FAS     | industry-articles/established-mining-industry-article/                |
            | DEV         | FAS     | industry-articles/global-humanitarian-support-article/                |
            | DEV         | FAS     | industry-articles/global-rail-experience-article/                     |
            | DEV         | FAS     | industry-articles/helping-you-buy-from-the-uk-article-ukef/           |
            | DEV         | FAS     | industry-articles/highly-rated-primary-care/                          |
            | DEV         | FAS     | industry-articles/home-of-oil-and-gas-innovation-article/             |
            | DEV         | FAS     | industry-articles/how-education-is-going-digital/                     |
            | DEV         | FAS     | industry-articles/how-tech-is-changing-the-way-we-bank-article/       |
            | DEV         | FAS     | industry-articles/innovative-airport-solutions-article/               |
            | DEV         | FAS     | industry-articles/leading-the-world-in-cancer-care/                   |
            | DEV         | FAS     | industry-articles/life-changing-artificial-intelligence-AI/           |
            | DEV         | FAS     | industry-articles/the-changing-face-of-visual-effects/                |
            | DEV         | FAS     | industry-articles/trusted-construction-partners-article/              |
            | DEV         | FAS     | industry-articles/uk-centres-of-excellence/                           |
            | DEV         | FAS     | industry-articles/uk-cyber-security-hubs/                             |
            | DEV         | FAS     | industry-articles/world-class-research-centre-article/                |
            | DEV         | FAS     | suppliers/00392279/contact/                                           |
            | DEV         | FAS     | suppliers/00392279/gl-events-uk-limited/                              |


        Examples: <environment> <service>
            | environment | service | page                                                                  |
            | STAGE       | FAS     | /                                                                     |
            | STAGE       | FAS     | case-study/1000/an-international-profession/                          |
            | STAGE       | FAS     | case-study/1004/england-and-wales-a-global-legal-centre/              |
            | STAGE       | FAS     | case-study/1010/port-comprehensive-assessment-operations-and-manag/   |
            | STAGE       | FAS     | case-study/102/livingskin-for-passive-prostheses/                     |
            | STAGE       | FAS     | case-study/1022/spl-launches-brochure-for-the-homebrew-industry/      |
            | STAGE       | FAS     | case-study/23/bp/                                                     |
            | STAGE       | FAS     | case-study/230/poland-sees-its-first-bio-diesel-generators/           |
            | STAGE       | FAS     | feedback/                                                             |
            | STAGE       | FAS     | industries/                                                           |
            | STAGE       | FAS     | industries/aerospace/                                                 |
            | STAGE       | FAS     | industries/agritech/                                                  |
            | STAGE       | FAS     | industries/automotive/                                                |
            | STAGE       | FAS     | industries/business-and-government-partnerships/                      |
            | STAGE       | FAS     | industries/business-and-government-partnerships/needs                 |
            | STAGE       | FAS     | industries/consumer-retail/                                           |
            | STAGE       | FAS     | industries/contact/                                                   |
            | STAGE       | FAS     | industries/contact/aerospace/                                         |
            | STAGE       | FAS     | industries/contact/agritech/                                          |
            | STAGE       | FAS     | industries/contact/automotive/                                        |
            | STAGE       | FAS     | industries/contact/business-and-government-partnerships/              |
            | STAGE       | FAS     | industries/contact/consumer-retail/                                   |
            | STAGE       | FAS     | industries/contact/creative-services/                                 |
            | STAGE       | FAS     | industries/contact/cyber-security/                                    |
            | STAGE       | FAS     | industries/contact/education-industry/                                |
            | STAGE       | FAS     | industries/contact/energy/                                            |
            | STAGE       | FAS     | industries/contact/engineering-industry/                              |
            | STAGE       | FAS     | industries/contact/food-and-drink/                                    |
            | STAGE       | FAS     | industries/contact/healthcare/                                        |
            | STAGE       | FAS     | industries/contact/infrastructure/                                    |
            | STAGE       | FAS     | industries/contact/innovation-industry/                               |
            | STAGE       | FAS     | industries/contact/legal-services/                                    |
            | STAGE       | FAS     | industries/contact/life-sciences/                                     |
            | STAGE       | FAS     | industries/contact/marine/                                            |
            | STAGE       | FAS     | industries/contact/professional-and-financial-services/               |
            | STAGE       | FAS     | industries/contact/space/                                             |
            | STAGE       | FAS     | industries/contact/sports-economy/                                    |
            | STAGE       | FAS     | industries/contact/technology/                                        |
            | STAGE       | FAS     | industries/creative-services/                                         |
            | STAGE       | FAS     | industries/cyber-security/                                            |
            | STAGE       | FAS     | industries/education-industry/                                        |
            | STAGE       | FAS     | industries/energy/                                                    |
            | STAGE       | FAS     | industries/engineering-industry/                                      |
            | STAGE       | FAS     | industries/food-and-drink/                                            |
            | STAGE       | FAS     | industries/healthcare/                                                |
            | STAGE       | FAS     | industries/infrastructure/                                            |
            | STAGE       | FAS     | industries/innovation-industry/                                       |
            | STAGE       | FAS     | industries/legal-services/                                            |
            | STAGE       | FAS     | industries/life-sciences/                                             |
            | STAGE       | FAS     | industries/marine/                                                    |
            | STAGE       | FAS     | industries/professional-and-financial-services/                       |
            | STAGE       | FAS     | industries/space/                                                     |
            | STAGE       | FAS     | industries/sports-economy/                                            |
            | STAGE       | FAS     | industries/technology/                                                |
            | STAGE       | FAS     | industry-articles/UK-agritech-strengths-article/                      |
            | STAGE       | FAS     | industry-articles/a-focus-on-regulatory-technology-solutions-article/ |
            | STAGE       | FAS     | industry-articles/a-global-centre-for-life-sciences/                  |
            | STAGE       | FAS     | industry-articles/building-fintech-bridges-article/                   |
            | STAGE       | FAS     | industry-articles/established-mining-industry-article/                |
            | STAGE       | FAS     | industry-articles/global-humanitarian-support-article/                |
            | STAGE       | FAS     | industry-articles/global-rail-experience-article/                     |
            | STAGE       | FAS     | industry-articles/helping-you-buy-from-the-uk-article-ukef/           |
            | STAGE       | FAS     | industry-articles/highly-rated-primary-care/                          |
            | STAGE       | FAS     | industry-articles/home-of-oil-and-gas-innovation-article/             |
            | STAGE       | FAS     | industry-articles/how-education-is-going-digital/                     |
            | STAGE       | FAS     | industry-articles/how-tech-is-changing-the-way-we-bank-article/       |
            | STAGE       | FAS     | industry-articles/innovative-airport-solutions-article/               |
            | STAGE       | FAS     | industry-articles/leading-the-world-in-cancer-care/                   |
            | STAGE       | FAS     | industry-articles/life-changing-artificial-intelligence-AI/           |
            | STAGE       | FAS     | industry-articles/the-changing-face-of-visual-effects/                |
            | STAGE       | FAS     | industry-articles/trusted-construction-partners-article/              |
            | STAGE       | FAS     | industry-articles/uk-centres-of-excellence/                           |
            | STAGE       | FAS     | industry-articles/uk-cyber-security-hubs/                             |
            | STAGE       | FAS     | industry-articles/world-class-research-centre-article/                |
            | STAGE       | FAS     | suppliers/00392279/contact/                                           |
            | STAGE       | FAS     | suppliers/00392279/gl-events-uk-limited/                              |


        Examples: <environment> <service>
            | environment | service | page                                                                  |
            | DEV         | ExRead  | /                                                                     |
            | DEV         | ExRead  | about/                                                                |
            | DEV         | ExRead  | business-planning/                                                    |
            | DEV         | ExRead  | customer-insight/                                                     |
            | DEV         | ExRead  | export-opportunities/                                                 |
            | DEV         | ExRead  | finance/                                                              |
            | DEV         | ExRead  | get-finance/                                                          |
            | DEV         | ExRead  | getting-paid/                                                         |
            | DEV         | ExRead  | international/                                                        |
            | DEV         | ExRead  | international/privacy-and-cookies/                                    |
            | DEV         | ExRead  | international/terms-and-conditions/                                   |
            | DEV         | ExRead  | market-research/                                                      |
            | DEV         | ExRead  | new/                                                                  |
            | DEV         | ExRead  | occasional/                                                           |
            | DEV         | ExRead  | operations-and-compliance/                                            |
            | DEV         | ExRead  | performance-dashboard/                                                |
            | DEV         | ExRead  | privacy-and-cookies/                                                  |
            | DEV         | ExRead  | regular/                                                              |
            | DEV         | ExRead  | story/hello-babys-rapid-online-growth/                                |
            | DEV         | ExRead  | story/online-marketplaces-propel-freestyle-xtreme-sales/              |
            | DEV         | ExRead  | story/york-bag-retailer-goes-global-via-e-commerce/                   |
            | DEV         | ExRead  | terms-and-conditions/                                                 |
            | DEV         | ExRead  | triage/                                                               |
            | DEV         | ExRead  | triage/exported-before/                                               |


        Examples: <environment> <service>
            | environment | service | page                                                                  |
            | STAGE       | ExRead  | /                                                                     |
            | STAGE       | ExRead  | about/                                                                |
            | STAGE       | ExRead  | business-planning/                                                    |
            | STAGE       | ExRead  | customer-insight/                                                     |
            | STAGE       | ExRead  | export-opportunities/                                                 |
            | STAGE       | ExRead  | finance/                                                              |
            | STAGE       | ExRead  | get-finance/                                                          |
            | STAGE       | ExRead  | getting-paid/                                                         |
            | STAGE       | ExRead  | international/                                                        |
            | STAGE       | ExRead  | international/privacy-and-cookies/                                    |
            | STAGE       | ExRead  | international/terms-and-conditions/                                   |
            | STAGE       | ExRead  | market-research/                                                      |
            | STAGE       | ExRead  | new/                                                                  |
            | STAGE       | ExRead  | occasional/                                                           |
            | STAGE       | ExRead  | operations-and-compliance/                                            |
            | STAGE       | ExRead  | performance-dashboard/                                                |
            | STAGE       | ExRead  | privacy-and-cookies/                                                  |
            | STAGE       | ExRead  | regular/                                                              |
            | STAGE       | ExRead  | story/hello-babys-rapid-online-growth/                                |
            | STAGE       | ExRead  | story/online-marketplaces-propel-freestyle-xtreme-sales/              |
            | STAGE       | ExRead  | story/york-bag-retailer-goes-global-via-e-commerce/                   |
            | STAGE       | ExRead  | terms-and-conditions/                                                 |
            | STAGE       | ExRead  | triage/                                                               |
            | STAGE       | ExRead  | triage/exported-before/                                               |


        Examples: <environment> <service>
            | environment | service | page                     |
            | DEV         | SSO     | /                        |
            | DEV         | SSO     | accounts/login/          |
            | DEV         | SSO     | accounts/password/reset/ |
            | DEV         | SSO     | accounts/signup/         |


        Examples: <environment> <service>
            | environment | service | page                     |
            | STAGE       | SSO     | /                        |
            | STAGE       | SSO     | accounts/login/          |
            | STAGE       | SSO     | accounts/password/reset/ |
            | STAGE       | SSO     | accounts/signup/         |


        Examples: <environment> <service>
            | environment | service | page   |
            | DEV         | Profile | /      |
            | DEV         | Profile | about/ |


        Examples: <environment> <service>
            | environment | service | page   |
            | STAGE       | Profile | /      |
            | STAGE       | Profile | about/ |


        @bug
        @TT-367
        @fixed
        Examples: <environment> <service>
            | environment | service | page                                                                          |
            | DEV         | SOO     | /                                                                             |
            | DEV         | SOO     | markets/shortlist/                                                            |
            | DEV         | SOO     | markets/story/chiswick-retailer-strikes-deal-with-amazon-australia/           |
            | DEV         | SOO     | markets/story/global-marketplaces-drive-burlingham-london-to-success/         |
            | DEV         | SOO     | markets/story/red-herring-games-take-their-mysteries-overseas-through-amazon/ |


        @bug
        @TT-367
        @fixed
        Examples: <environment> <service>
            | environment | service | page                                                                          |
            | STAGE       | SOO     | /                                                                             |
            | STAGE       | SOO     | markets/shortlist/                                                            |
            | STAGE       | SOO     | markets/story/chiswick-retailer-strikes-deal-with-amazon-australia/           |
            | STAGE       | SOO     | markets/story/global-marketplaces-drive-burlingham-london-to-success/         |
            | STAGE       | SOO     | markets/story/red-herring-games-take-their-mysteries-overseas-through-amazon/ |


        @bug
        @XOT-418
        @fixme
        @NO_X_TAG_HEADER
        Examples: <environment> <service>
            | environment | service | page                                            |
            | DEV         | ExOpps  | /                                               |
            | DEV         | ExOpps  | opportunities/                                  |
            | DEV         | ExOpps  | opportunities?sectors[]=creative-media          |
            | DEV         | ExOpps  | opportunities?sectors[]=education-training      |
            | DEV         | ExOpps  | opportunities/framework-agreement-meat-and-fish |


        @bug
        @XOT-418
        @fixme
        @NO_X_TAG_HEADER
        Examples: <environment> <service>
            | environment | service | page                                            |
            | STAGE       | ExOpps  | /                                               |
            | STAGE       | ExOpps  | opportunities/                                  |
            | STAGE       | ExOpps  | opportunities?sectors[]=creative-media          |
            | STAGE       | ExOpps  | opportunities?sectors[]=education-training      |
            | STAGE       | ExOpps  | opportunities/framework-agreement-meat-and-fish |
