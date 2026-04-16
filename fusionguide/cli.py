import click


@click.group()
def cli():
    """FusionGuide — Bayesian Active Learning for fusion experiments."""


@cli.command()
@click.option("--material", type=click.Choice(["vanadium_alloy", "ceramic_insulator", "rafm_steel"]), default="vanadium_alloy")
@click.option("--n", default=3, help="Number of recommendations")
@click.option("--prior-parquet", default=None, help="Path to FusionMatDB Parquet export")
def recommend(material, n, prior_parquet):
    """Get experiment recommendations for a material system."""
    import pandas as pd
    from fusionguide.campaign import FusionCampaign
    from fusionguide.spaces.vanadium_alloy import VanadiumAlloySpace
    from fusionguide.spaces.ceramic_insulator import CeramicInsulatorSpace
    from fusionguide.spaces.rafm_steel import RAFMSteelSpace
    from fusionguide.targets.mechanical import YieldStrengthTarget, DielectricStrengthTarget

    if material == "vanadium_alloy":
        params = VanadiumAlloySpace()
        target = YieldStrengthTarget()
    elif material == "rafm_steel":
        params = RAFMSteelSpace()
        target = YieldStrengthTarget()
    else:
        params = CeramicInsulatorSpace()
        target = DielectricStrengthTarget()

    prior = None
    if prior_parquet:
        from fusionguide.priors.fusionmatdb import load_prior_from_parquet
        prior = load_prior_from_parquet(prior_parquet, material_class=material)
        click.echo(f"Loaded {len(prior)} prior measurements from FusionMatDB")

    campaign = FusionCampaign(name=f"cli_{material}", parameters=params, target=target, prior_data=prior)
    recs = campaign.recommend(n=n)
    click.echo(f"\nTop {n} recommended experiments for {material}:")
    click.echo(recs.to_string(index=False))


@cli.command()
@click.option("--timeline", default=18, help="Max queue time in months")
@click.option("--samples", default=20, help="Number of samples")
@click.option("--budget", default=200.0, help="Budget (relative, ion_beam=1)")
def facilities(timeline, samples, budget):
    """Recommend irradiation facilities for your experiment."""
    from fusionguide.facility_scheduler import recommend_facility
    recs = recommend_facility(timeline_months=timeline, n_samples=samples, budget_relative=budget)
    if not recs:
        click.echo("No suitable facilities found for given constraints.")
        return
    for r in recs:
        click.echo(f"  {r.facility:<10} fidelity={r.fidelity:.0%}  queue={r.queue_months}mo  {r.rationale}")


def main():
    cli()
