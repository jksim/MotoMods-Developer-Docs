"""Curated map from original developer.motorola.com paths to the rebuilt site.

`SOURCE` names the snapshot page each doc is built from. Where the 2017 Drupal
portal revised a page substantially (its Debug and Log and MDK Overview are
several times longer than the Squarespace originals) the Drupal capture wins;
where it merely reflowed identical text, the Squarespace original wins and the
Drupal copy survives only in archive/.
"""

# (original path, output markdown path, nav title)
PAGES = [
    ('get-started',                                 'get-started.md',                               'Get Started'),

    ('explore',                                     'explore/index.md',                             'Overview'),
    ('explore/intro',                               'explore/introduction.md',                      'Introduction'),
    ('explore/system-architecture',                 'explore/system-architecture.md',               'System Architecture'),

    ('explore/firmware',                            'explore/firmware/index.md',                    'Overview'),
    ('explore/firmware/mod-management',             'explore/firmware/mod-management.md',           'Mod Management'),
    ('explore/firmware/power-transfer',             'explore/firmware/power-transfer.md',           'Power Transfer'),
    ('explore/firmware/battery',                    'explore/firmware/battery.md',                  'Battery'),
    ('explore/firmware/display',                    'explore/firmware/display.md',                  'Display'),
    ('explore/firmware/audio',                      'explore/firmware/audio.md',                    'Audio'),
    ('explore/firmware/hid',                        'explore/firmware/hid.md',                      'HID'),
    ('explore/firmware/usb-ext',                    'explore/firmware/usb-ext.md',                  'USB-Ext'),
    ('explore/firmware/raw',                        'explore/firmware/raw.md',                      'Raw'),
    ('explore/firmware/lights',                     'explore/firmware/lights.md',                   'Lights'),
    ('explore/firmware/camera-ext/camera-controls', 'explore/firmware/camera-controls.md',          'Camera Controls'),

    ('explore/software',                            'explore/software/index.md',                    'Overview'),
    ('explore/software/mod-management',             'explore/software/mod-management.md',           'Mod Management'),
    ('explore/software/mod-raw-devices',            'explore/software/mod-raw-devices.md',          'Mod Raw Devices'),
    ('explore/software/mod-display',                'explore/software/mod-display.md',              'Mod Display'),
    ('explore/software/mod-battery',                'explore/software/mod-battery.md',              'Mod Battery'),
    ('explore/software/mod-audio',                  'explore/software/mod-audio.md',                'Mod Audio'),
    ('explore/software/mod-hid',                    'explore/software/mod-hid.md',                  'Mod HID'),
    ('explore/software/mod-usb',                    'explore/software/mod-usb.md',                  'Mod USB'),

    ('build',                                       'build/index.md',                               'Overview'),
    ('build/intro',                                 'build/introduction.md',                        'Introduction'),

    ('documentation/mdk-overview',                  'build/mdk-user-guide/index.md',                'MDK Overview'),
    ('build/mdk-user-guide',                        'build/mdk-user-guide/reference-moto-mod.md',   'Reference Moto Mod'),
    ('build/mdk-user-guide/perforated-board',       'build/mdk-user-guide/perforated-board.md',     'Perforated Board'),
    ('build/mdk-user-guide/hat-adapter-board',      'build/mdk-user-guide/hat-adapter-board.md',    'HAT Adapter Board'),
    ('build/mdk-user-guide/custom-circuit-board',   'build/mdk-user-guide/custom-circuit-board.md', 'Custom Circuit Board'),

    ('build/tools',                                 'build/tools/index.md',                         'Overview'),
    ('build/tools/setup-environment',               'build/tools/setup-environment.md',             'Set Up Your Environment'),
    ('build/tools/build-from-source',               'build/tools/build-from-source.md',             'Build from Source'),
    ('build/tools/flashing-firmware',               'build/tools/flashing-firmware.md',             'Flashing Firmware'),
    ('documentation/debug-and-log',                 'build/tools/debug-and-log.md',                 'Debug and Log'),

    ('build/examples',                              'build/examples/index.md',                      'Overview'),
    ('build/examples/hello-world',                  'build/examples/hello-world.md',                'Hello World'),
    ('build/examples/mdk-utility',                  'build/examples/mdk-utility.md',                'MDK Utility'),
    ('build/examples/audio',                        'build/examples/audio.md',                      'Audio Personality Card'),
    ('build/examples/battery',                      'build/examples/battery.md',                    'Battery Personality Card'),
    ('build/examples/display',                      'build/examples/display.md',                    'Display Personality Card'),
    ('build/examples/sensor',                       'build/examples/sensor.md',                     'Sensor Personality Card'),
    ('build/examples/camera-hat',                   'build/examples/camera-hat.md',                 'Camera with HAT Adapter'),
    ('build/examples/misc',                         'build/examples/misc.md',                       'Miscellaneous'),

    ('products',                                    'hardware/index.md',                            'Overview'),
    ('products/mdk',                                'hardware/mdk.md',                              'Moto Mods Development Kit'),
    ('products/perforated-board',                   'hardware/perforated-board.md',                 'Perforated Board'),
    ('products/hat-adapter-board',                  'hardware/hat-adapter-board.md',                'HAT Adapter Board'),
    ('products/audio-personality-card',             'hardware/audio-personality-card.md',           'Audio Personality Card'),
    ('products/battery-personality-card',           'hardware/battery-personality-card.md',         'Battery Personality Card'),
    ('products/display-personality-card',           'hardware/display-personality-card.md',         'Display Personality Card'),
    ('products/temperature-sensor-personality-card','hardware/temperature-sensor-personality-card.md','Temperature Sensor Personality Card'),
    ('tools-kits',                                  'hardware/tools-and-kits.md',                   'Tools & Kits'),
    ('buy',                                         'hardware/where-to-buy.md',                     'Where to Buy'),

    ('documentation/all-downloads',                 'downloads.md',                                 'Downloads'),

    ('partner/overview',                            'partner/index.md',                             'Overview'),
    ('partner',                                     'partner/certification-program.md',             'Certification Program'),
    ('partner/certification-guidelines',            'partner/certification-guidelines.md',          'Certification Guidelines'),
    ('partner/contact-form',                        'partner/contact.md',                           'Contact'),

    ('support',                                     'support/index.md',                             'Overview'),
    ('support/faq',                                 'support/faq.md',                               'FAQ'),
]

# Original paths that survive only as raw HTML in archive/ — the 2017 Drupal
# portal's reflowed duplicates of pages already covered above.
ARCHIVE_ONLY = [
    'documentation', 'documentation/mdk-overview-0', 'documentation/system-architecture',
    'documentation/mod-hid', 'documentation/mod-usb', 'documentation/perforated-board',
    'documentation/mdk-utility', 'documentation/examples-overview',
    'documentation/flashing-firmware', 'build/tools/debug-and-log', 'build/overview',
]

# Original paths that no longer have a page of their own; links to them are
# redirected to the nearest surviving equivalent.
REDIRECTS = {
    'documentation': 'explore/index.md',
    'documentation/mdk-overview-0': 'build/mdk-user-guide/index.md',
    'documentation/system-architecture': 'explore/system-architecture.md',
    'documentation/mod-hid': 'explore/software/mod-hid.md',
    'documentation/mod-usb': 'explore/software/mod-usb.md',
    'documentation/perforated-board': 'build/mdk-user-guide/perforated-board.md',
    'documentation/mdk-utility': 'build/examples/mdk-utility.md',
    'documentation/examples-overview': 'build/examples/index.md',
    'documentation/flashing-firmware': 'build/tools/flashing-firmware.md',
    'build/tools/debug-and-log': 'build/tools/debug-and-log.md',
    'build/overview': 'build/mdk-user-guide/index.md',
    'home': 'index.md',
    '': 'index.md',
}

NAV = [
    ('Home', 'index.md'),
    ('Get Started', 'get-started.md'),
    ('Explore the Platform', [
        ('Overview', 'explore/index.md'),
        ('Introduction', 'explore/introduction.md'),
        ('System Architecture', 'explore/system-architecture.md'),
        ('Firmware Protocols', [
            ('Overview', 'explore/firmware/index.md'),
            ('Mod Management', 'explore/firmware/mod-management.md'),
            ('Power Transfer', 'explore/firmware/power-transfer.md'),
            ('Battery', 'explore/firmware/battery.md'),
            ('Display', 'explore/firmware/display.md'),
            ('Audio', 'explore/firmware/audio.md'),
            ('HID', 'explore/firmware/hid.md'),
            ('USB-Ext', 'explore/firmware/usb-ext.md'),
            ('Raw', 'explore/firmware/raw.md'),
            ('Lights', 'explore/firmware/lights.md'),
            ('Camera Controls', 'explore/firmware/camera-controls.md'),
        ]),
        ('Android Software', [
            ('Overview', 'explore/software/index.md'),
            ('Mod Management', 'explore/software/mod-management.md'),
            ('Mod Raw Devices', 'explore/software/mod-raw-devices.md'),
            ('Mod Display', 'explore/software/mod-display.md'),
            ('Mod Battery', 'explore/software/mod-battery.md'),
            ('Mod Audio', 'explore/software/mod-audio.md'),
            ('Mod HID', 'explore/software/mod-hid.md'),
            ('Mod USB', 'explore/software/mod-usb.md'),
        ]),
    ]),
    ('Build a Prototype', [
        ('Overview', 'build/index.md'),
        ('Introduction', 'build/introduction.md'),
        ('MDK User Guide', [
            ('MDK Overview', 'build/mdk-user-guide/index.md'),
            ('Reference Moto Mod', 'build/mdk-user-guide/reference-moto-mod.md'),
            ('Perforated Board', 'build/mdk-user-guide/perforated-board.md'),
            ('HAT Adapter Board', 'build/mdk-user-guide/hat-adapter-board.md'),
            ('Custom Circuit Board', 'build/mdk-user-guide/custom-circuit-board.md'),
        ]),
        ('Developer Tools', [
            ('Overview', 'build/tools/index.md'),
            ('Set Up Your Environment', 'build/tools/setup-environment.md'),
            ('Build from Source', 'build/tools/build-from-source.md'),
            ('Flashing Firmware', 'build/tools/flashing-firmware.md'),
            ('Debug and Log', 'build/tools/debug-and-log.md'),
        ]),
        ('Examples', [
            ('Overview', 'build/examples/index.md'),
            ('Hello World', 'build/examples/hello-world.md'),
            ('MDK Utility', 'build/examples/mdk-utility.md'),
            ('Audio Personality Card', 'build/examples/audio.md'),
            ('Battery Personality Card', 'build/examples/battery.md'),
            ('Display Personality Card', 'build/examples/display.md'),
            ('Sensor Personality Card', 'build/examples/sensor.md'),
            ('Camera with HAT Adapter', 'build/examples/camera-hat.md'),
            ('Miscellaneous', 'build/examples/misc.md'),
        ]),
    ]),
    ('Hardware', [
        ('Overview', 'hardware/index.md'),
        ('Moto Mods Development Kit', 'hardware/mdk.md'),
        ('Perforated Board', 'hardware/perforated-board.md'),
        ('HAT Adapter Board', 'hardware/hat-adapter-board.md'),
        ('Audio Personality Card', 'hardware/audio-personality-card.md'),
        ('Battery Personality Card', 'hardware/battery-personality-card.md'),
        ('Display Personality Card', 'hardware/display-personality-card.md'),
        ('Temperature Sensor Personality Card', 'hardware/temperature-sensor-personality-card.md'),
        ('Tools & Kits', 'hardware/tools-and-kits.md'),
        ('Where to Buy', 'hardware/where-to-buy.md'),
    ]),
    ('Downloads', 'downloads.md'),
    ('Partner & Certification', [
        ('Overview', 'partner/index.md'),
        ('Certification Program', 'partner/certification-program.md'),
        ('Certification Guidelines', 'partner/certification-guidelines.md'),
        ('License Agreement', 'partner/license-agreement.md'),
        ('Contact', 'partner/contact.md'),
    ]),
    ('Support', [
        ('Overview', 'support/index.md'),
        ('FAQ', 'support/faq.md'),
    ]),
    ('Legal', [
        ('MDK Terms & Conditions', 'legal/mdk-terms-and-conditions.md'),
    ]),
    ('About This Archive', 'about.md'),
]
