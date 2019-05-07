Feature: Find content differences between Staging and DEV International environments

  Scenario Outline: Content on Staging page "<selected>" should be the same as on respective Dev page
    When you look at the "main" section of the "<selected>" page on "International" "STAGE" and "DEV"

    Then there should be no differences

    Examples: International
      | selected                                  |
      | /                                         |
      | ?lang=de                                  |
      | ?lang=zh-hans                             |
      | industries/                               |
      | industries/engineering-and-manufacturing/ |
      | industries/healthcare-and-life-sciences/  |
