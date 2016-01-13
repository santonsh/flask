from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
street_light = Table('street_light', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('idOnController', String(length=64)),
    Column('controllerStrId', String(length=64)),
    Column('MacAddress', String(length=64)),
    Column('address', String(length=64)),
    Column('Latitude', Float),
    Column('Longitude', Float),
    Column('dimmingGroupName', String(length=64)),
    Column('brandId', Integer),
    Column('categoryStrId', Integer),
    Column('modelFunctionId', Integer),
    Column('comment', String(length=256)),
    Column('install_date', String(length=32)),
    Column('InstallStatus', String(length=32)),
    Column('network_section', String(length=32)),
    Column('network_segmentnumber', Integer),
    Column('network_type', String(length=32)),
    Column('power', Integer),
    Column('powerCorrection', Integer),
    Column('ProductId', String(length=32)),
    Column('providerId', Integer),
    Column('reference', Integer),
    Column('SoftwareVersion', String(length=32)),
    Column('SystemInfo', String(length=128)),
    Column('pole_numberoflight', Integer),
    Column('pole_type', String(length=32)),
    Column('ballast_brand', String(length=32)),
    Column('ballast_type', String(length=32)),
    Column('luminaire_brand', String(length=32)),
    Column('luminaire_colorcode', String(length=32)),
    Column('luminaire_function', String(length=32)),
    Column('luminaire_model', String(length=32)),
    Column('luminaire_status', String(length=32)),
    Column('LampLevel', Float),
    Column('LampSwitch', Boolean),
    Column('LampCommandLevel', Float),
    Column('LampCommandMode', Integer),
    Column('LampCommandSwitch', Float),
    Column('RunningHours', Float),
    Column('Current', Float),
    Column('LampCurrent', Float),
    Column('MainVoltage', Float),
    Column('LampVoltage', Float),
    Column('MeteredPower', Float),
    Column('LampPower', Float),
    Column('Energy', Float),
    Column('LampEnergy', Float),
    Column('LampRestartCount', Integer),
    Column('CycleCount', Integer),
    Column('BallastTemp', Float),
    Column('DryContactInput', Boolean),
    Column('PowerFactor', Float),
    Column('Temperature', Float),
    Column('Frequency', Float),
    Column('LampFailure', Boolean),
    Column('BallastCommunicationFailure', Boolean),
    Column('BallastFailure', Boolean),
    Column('CapacitorFailure', Boolean),
    Column('CommissioningFailed', Boolean),
    Column('DaliFailure', Boolean),
    Column('DefaultLostNode', Boolean),
    Column('DeviceFailure', Boolean),
    Column('ExternalComFailure', Boolean),
    Column('FlickeringFailure', Boolean),
    Column('HighCurrent', Boolean),
    Column('LowCurrent', Boolean),
    Column('HighLampCurrent', Boolean),
    Column('LowLampCurrent', Boolean),
    Column('HighVoltage', Boolean),
    Column('LowVoltage', Boolean),
    Column('HighLampVoltage', Boolean),
    Column('LowLampVoltage', Boolean),
    Column('HighPower', Boolean),
    Column('LowPower', Boolean),
    Column('LowPowerFactor', Boolean),
    Column('HighLampRunningHours', Boolean),
    Column('HighBallastTemperature', Boolean),
    Column('HighOLCTemperature', Boolean),
    Column('PhotocellStatus', Boolean),
    Column('PhotocellFailure', Boolean),
    Column('RelayFailure', Boolean),
    Column('BackupScheduler', Boolean),
    Column('LED_temperature', Float),
    Column('Latitude_GPS', Float),
    Column('Longitude_GPS', Float),
    Column('Angle_roll', Float),
    Column('Angle_pitch', Float),
    Column('peripherial_A', Float),
    Column('peripherial_B', Float),
    Column('air_quality_pm25', Float),
    Column('air_quality_pm10', Float),
    Column('humidity', Float),
    Column('outside_temp', Float),
    Column('noise_pollution', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['street_light'].columns['Angle_pitch'].create()
    post_meta.tables['street_light'].columns['Angle_roll'].create()
    post_meta.tables['street_light'].columns['LED_temperature'].create()
    post_meta.tables['street_light'].columns['Latitude_GPS'].create()
    post_meta.tables['street_light'].columns['Longitude_GPS'].create()
    post_meta.tables['street_light'].columns['air_quality_pm10'].create()
    post_meta.tables['street_light'].columns['air_quality_pm25'].create()
    post_meta.tables['street_light'].columns['humidity'].create()
    post_meta.tables['street_light'].columns['noise_pollution'].create()
    post_meta.tables['street_light'].columns['outside_temp'].create()
    post_meta.tables['street_light'].columns['peripherial_A'].create()
    post_meta.tables['street_light'].columns['peripherial_B'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['street_light'].columns['Angle_pitch'].drop()
    post_meta.tables['street_light'].columns['Angle_roll'].drop()
    post_meta.tables['street_light'].columns['LED_temperature'].drop()
    post_meta.tables['street_light'].columns['Latitude_GPS'].drop()
    post_meta.tables['street_light'].columns['Longitude_GPS'].drop()
    post_meta.tables['street_light'].columns['air_quality_pm10'].drop()
    post_meta.tables['street_light'].columns['air_quality_pm25'].drop()
    post_meta.tables['street_light'].columns['humidity'].drop()
    post_meta.tables['street_light'].columns['noise_pollution'].drop()
    post_meta.tables['street_light'].columns['outside_temp'].drop()
    post_meta.tables['street_light'].columns['peripherial_A'].drop()
    post_meta.tables['street_light'].columns['peripherial_B'].drop()
